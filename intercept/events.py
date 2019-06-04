# Stdlib
from dataclasses import field, dataclass
from typing import Any, Dict, List

# Intercept Client Internals
from intercept.utils import REGEXES


@dataclass
class Event:
    event: str


@dataclass
class MessageEvent(Event):
    event: str
    msg: str


@dataclass
class InfoEvent(Event):
    event: str
    client_id: str
    client_type: str
    connected_at: int
    date: int


@dataclass
class AuthEvent(Event):
    event: str
    success: bool
    token: str = None
    player: str = None


@dataclass
class SystemInfo:
    id: str
    ip: str
    hostname: str
    type: str


@dataclass
class SystemEvent(Event):
    event: str
    success: bool
    systems: List[SystemInfo] = field(default_factory=list)

    def __post_init__(self):
        self.systems = list(map(lambda x: SystemInfo(**x), self.systems))


@dataclass
class ConnectEvent(Event):
    event: str
    success: bool
    cfg: Dict[str, Any] = field(default_factory=dict)
    clink: List[str] = field(default_factory=list)


@dataclass
class ConnectedEvent(Event):
    event: str
    hostname: str
    user: str
    access: bool


@dataclass
class CommandEvent(Event):
    event: str
    success: bool
    cmd: str


@dataclass
class BroadcastEvent(MessageEvent):
    event: str
    msg: str


@dataclass
class TraceStartEvent(MessageEvent):
    event: str
    system: str
    panic: bool
    msg: str


@dataclass
class TraceCompleteEvent(MessageEvent):
    event: str
    system: str
    panicEnd: bool
    msg: str


@dataclass
class ChatEvent(MessageEvent):
    event: str
    msg: str

    @property
    def chat(self) -> str:
        return REGEXES["chat_event"].match(self.msg).group("chat")

    @property
    def author(self) -> str:
        return REGEXES["chat_event"].match(self.msg).group("author")

    @property
    def message(self) -> str:
        return REGEXES["chat_event"].match(self.msg).group("message")


@dataclass
class ErrorEvent(Event):
    event: str
    success: bool
    error: str


@dataclass
class ConfigEvent(Event):
    event: str
    cfg: Dict[str, Any] = field(default_factory=dict)
