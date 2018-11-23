import anyio
from discord import Client as DClient, Message

from intercept import Client, DataFormat, ChatEvent

# Intercept settings
username = "abc"
password = "abc"
chat_name = "mychat"

# Discord settings
token = "discord_token"
channel_id = 123456789

client = Client(username, password, handle_data=DataFormat.CLEAN)
discord_client = DClient()


@client.event
async def event_chat(event: ChatEvent):
    if event.chat == chat_name and event.author != username:
        target_channel = await discord_client.get_channel(channel_id)
        await target_channel.send(f"{event.author}: {event.message}")


@discord_client.event
async def on_message(message: Message):
    if message.channel.id == channel_id and not message.author.bot:
        msg = f"{message.author}: {message.clean_content}"
        await client.command(f"chats send {chat_name} {msg}")


async def start_both():
    with anyio.create_task_group() as tg:
        tg.spawn(discord_client.run, token)
        await client.start()


anyio.run(start_both, backend="asyncio")
