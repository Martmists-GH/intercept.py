# flake8: noqa
# pylint: skip-file

# Intercept Client Internals
from intercept import Client, ChatEvent, DataFormat

username = "abc"
password = "abc"

client = Client(username, password, handle_data=DataFormat.CLEAN)


@client.event
async def event_chat(event: ChatEvent):
    print(event.msg)


client.run()
