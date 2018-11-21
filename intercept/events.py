# Stdlib
from dataclasses import field, dataclass
from typing import Any, Dict


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
    token: str
    cfg: dict


@dataclass
class ConnectData:
    ip: str
    conn: str


@dataclass
class ConnectEvent(MessageEvent):
    event: str
    success: bool
    msg: str
    player: ConnectData
    cfg: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CommandEvent(MessageEvent):
    event: str
    success: bool
    cmd: str
    msg: str


@dataclass
class ConnectedEvent(Event):
    event: str
    player: ConnectData


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
