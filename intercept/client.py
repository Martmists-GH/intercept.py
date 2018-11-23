# Stdlib
import inspect
from typing import T, Dict, Callable

# External Libraries
import anyio

# Intercept Client Internals
from intercept.api_handler import APIHandler
from intercept.data_format import DataFormat
from intercept.events import Event, AuthEvent, CommandEvent, MessageEvent


class Client:
    def __init__(self, username: str, password: str, register: bool = False,
                 handle_data: DataFormat = DataFormat.CLEAN):
        self.username = username
        self.password = password
        self.register = register

        self.handler = APIHandler(self, handle_data)
        self._events: Dict[str, Callable[[Event], None]] = {}

    def event(self, func: Callable[[Event], None]):
        fname = func.__name__
        self._events[fname] = func

    def __getattr__(self, item):
        if item in self._events:
            return self._events[item]
        return super().__getattribute__(item)

    async def wait_for(self, event=None, command=None, type_: T = Event) -> T:
        return await self.handler.wait_for(event, command, type_)

    async def command(self, command: str) -> CommandEvent:
        self.handler.send_data({
            "request": "command",
            "cmd": command.strip()
        })

        key = command.split()[0]
        return await self.wait_for(command=key, type_=CommandEvent)

    async def login(self):
        key = "register" if self.register else "login"

        self.handler.send_data({
            "request": "auth",
            key: {
                "username": self.username,
                "password": self.password
            }
        })

        auth = await self.wait_for(event="auth", type_=AuthEvent)

        self.handler.send_data({
            "request": "connect",
            "token": auth.token
        })

        await self.wait_for(event="connect")

        if hasattr(self, "event_ready"):
            func = getattr(self, "event_ready")
            res = func()
            if inspect.isawaitable(res):
                await res

    async def start(self):
        async with anyio.create_task_group() as tg:
            await tg.spawn(self.handler.start)
            await self.login()

    def run(self, backend: str = 'asyncio'):
        try:
            anyio.run(self.start, backend=backend)
        except KeyboardInterrupt:
            pass

    def stop(self):
        self.handler.stop()

        # Send final event to close loop
        self.handler.send_data({
            "request": "command",
            "cmd": "broadcast disconnecting custom client..."
        })


if __name__ == "__main__":
    with open("config.txt") as f:
        client = Client(*f.read().split("|"), handle_data=DataFormat.ANSI)


    @client.event
    async def on_event(event):
        if isinstance(event, MessageEvent):
            print(event.msg)


    @client.event
    async def event_ready():
        await client.command("slaves list")
        # client.stop()


    client.run()
