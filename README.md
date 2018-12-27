# Intercept.py
Python library for [intercept](https://bubmet.itch.io/intercept), a game by [bubmet](https://github.com/bubmet).

Styled after [discord.py](https://github.com/Rapptz/discord.py), this library aims to give users a customizable experience with the game.

# Examples

Chat logger:
```py
from intercept import Client, DataFormat, ChatEvent

client = Client(username, password, handle_data=DataFormat.CLEAN)


@client.event
async def event_chat(event: ChatEvent):
    print(event.msg)

client.run()
```

Simple custom client using [prompt-toolkit](https://github.com/prompt-toolkit/python-prompt-toolkit):
```py
from prompt_toolkit import prompt
from prompt_toolkit.eventloop.defaults import use_asyncio_event_loop
from prompt_toolkit.patch_stdout import patch_stdout

from intercept import Client, DataFormat, MessageEvent

use_asyncio_event_loop()

client = Client(username, password, handle_data=DataFormat.ANSI)


@client.event
async def on_event(event):
    if isinstance(event, MessageEvent):
        print(event.msg)


@client.event
async def event_ready():
    while client.handler._do_loop:  # pylint: disable=protected-access
        with patch_stdout():
            text = await prompt(" >> ", async_=True)

        if text == "quit":
            client.stop()
        else:
            await client.command(text)
    print("Done running")


client.run(backend='asyncio')
```

More examples can be found [here](https://github.com/martmists/intercept.py/tree/master/examples).

Additionally, I've made a custom client for intercept using intercept.py, which can be found [here](https://github.com/martmists/intercept_python_client).
