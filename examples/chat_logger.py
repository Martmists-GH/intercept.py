from intercept import Client, DataFormat, ChatEvent

username = "abc"
password = "abc"

client = Client(username, password, handle_data=DataFormat.CLEAN)


@client.event
async def event_chat(event: ChatEvent):
    print(event.msg)


client.run()
