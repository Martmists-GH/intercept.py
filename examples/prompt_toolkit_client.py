# flake8: noqa
# pylint: skip-file

# External Libraries
from prompt_toolkit import prompt
from prompt_toolkit.eventloop.defaults import use_asyncio_event_loop
from prompt_toolkit.patch_stdout import patch_stdout

# Intercept Client Internals
from intercept import Client, DataFormat, MessageEvent

use_asyncio_event_loop()

username = "abc"
password = "abc"

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
