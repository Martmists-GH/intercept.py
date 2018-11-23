# Stdlib
import inspect
from typing import T, Any, Dict, List, Type

# External Libraries
import anyio

# Intercept Client Internals
from intercept.data_format import DataFormat
from intercept.events import (Event, AuthEvent, ChatEvent, InfoEvent, CommandEvent, ConnectEvent, BroadcastEvent,
                              ConnectedEvent, TraceStartEvent, TraceCompleteEvent)
from intercept.utils import without_color_codes, converted_color_codes

try:
    import ujson as json
except ImportError:
    import json
    print("Install ujson for a performance boost while reading data")


class APIHandler:
    HOST = "209.97.136.54"
    PORT = 13373

    EVENTS: Dict[str, Type[Event]] = {
        'info': InfoEvent,
        'auth': AuthEvent,
        'connect': ConnectEvent,
        'command': CommandEvent,
        'connected': ConnectedEvent,
        'broadcast': BroadcastEvent,
        'traceStart': TraceStartEvent,
        'traceComplete': TraceCompleteEvent,
        'chat': ChatEvent
    }

    def __init__(self, client, fmt: DataFormat = DataFormat.CLEAN, bot=True, bufsize: int = 2 ** 24):
        self.client = client
        self._bot = bot
        self._buf_size = bufsize
        self._do_loop = False
        self._end_loop = True
        self._sock: anyio.abc.SocketStream = None
        self._messages: List[bytes] = []
        self._locks: List[Dict[str, Any]] = []
        self._fmt = fmt
        self._task = None

    def _format(self, arg: str) -> str:
        if self._fmt == DataFormat.CLEAN:
            return without_color_codes(arg)
        if self._fmt == DataFormat.ANSI:
            return converted_color_codes(arg)
        return arg

    def _build_event(self, data: Dict[str, Any]) -> Event:
        event = data["event"]
        if event in self.EVENTS:
            return self.EVENTS[event](**data)

        print(f"Unhandled event: {event}")
        print(data)

    async def _read_loop(self):
        while self._do_loop:
            # Read a single line
            line = await self._sock.receive_until(b"\n", self._buf_size)

            if not line:
                print("Server shutting down.")
                self._do_loop = False
                break

            data = json.loads(line.decode('utf-8'))

            if "msg" in data:
                data["msg"] = self._format(data["msg"])

            event = data['event']
            built = self._build_event(data)

            if not built:
                continue

            if hasattr(self.client, f"event_{event}"):
                func = getattr(self.client, f"event_{event}")
                res = func(built)
                if inspect.isawaitable(res):
                    await res

            if hasattr(self.client, "on_event"):
                func = getattr(self.client, "on_event")
                res = func(built)
                if inspect.isawaitable(res):
                    await res

            if self._locks:
                for entry in self._locks:
                    if entry['function'](data):
                        self._locks.remove(entry)
                        entry["result"] = built
                        await entry['lock'].set()
        self._end_loop = True

    async def _write_loop(self):
        while not self._end_loop:
            if self._messages:
                msg = self._messages.pop(0)
                await self._sock.send_all(msg)
                await anyio.sleep(max(0.3, 0.05 * len(msg)))
            else:
                await anyio.sleep(0.01)

    async def wait_for(self, event=None, command=None, type_: T = Event) -> T:
        if event is not None:
            f = lambda x: x['event'] == event or (event == "command" and "error" in x and
                                                  x['error'] == "Invalid command")
        elif command is not None:
            f = lambda x: x.get('cmd') == command
        else:
            f = lambda: True

        lock = anyio.create_event()
        entry: Dict[str, Any] = {
            "function": f,
            "lock": lock,
            "result": None
        }

        self._locks.append(entry)
        await lock.wait()

        assert isinstance(entry["result"], type_)

        return entry["result"]

    async def start(self):
        self._do_loop = True
        self._end_loop = False
        await self.setup()
        async with anyio.create_task_group() as task_group:
            await task_group.spawn(self._read_loop)
            await task_group.spawn(self._write_loop)

    async def setup(self):
        self._sock = await anyio.connect_tcp(self.HOST, self.PORT)

    def _send(self, message: bytes):
        self._messages.append(message)

    def send_data(self, data: Dict[str, Any]):
        raw = json.dumps(data)
        self._send(raw.encode("utf-8"))

    def stop(self):
        self._do_loop = False
