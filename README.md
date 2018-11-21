# Intercept.py
Python library for [intercept](https://bubmet.itch.io/intercept), a game by [bubmet](https://github.com/bubmet)

Styled after [discord.py](https://github.com/Rapptz/discord.py) (async), this library aims to give users a customizable experience with the game.

# Examples

Chat logger:
```py
from intercept import Client, DataFormat, ChatEvent

client = Client(username, password, fmt=DataFormat.CLEAN)

@client.event
async def event_chat(event: ChatEvent):
    print(event.msg)

client.run()
```

Simple custom client:
```py
from prompt_toolkit import prompt
from intercept import Client, DataFormat, MessageEvent

client = Client(username, password, fmt=DataFormat.ANSI)

@client.event
async def on_event(event):
    if isinstance(event, MessageEvent):
        print(event.msg)

@client.event
async def event_ready():
    while client._do_loop:  # pylint: disable=protected-access
        text = await prompt(" >> ", async_=True)
        await client.command(text)

client.run(backend='asyncio')
```
