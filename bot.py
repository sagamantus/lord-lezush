import os, nextcord as discord
from nextcord.ext import commands, tasks
from utils.mobile_presence import identify
from utils import config
from utils.help import HelpCommand

discord.gateway.DiscordWebSocket.identify = identify

client = commands.Bot(command_prefix=config.PREFIX, help_command=HelpCommand(), intents=discord.Intents.all())

# Loading exts
for directory in os.listdir('exts'):
    if not directory.endswith(".py"):
        for file_name in os.listdir(f'exts/{directory}'):
            if file_name.endswith(".py") and not file_name.startswith(("__")):
                client.load_extension(f"exts.{directory}.{file_name[:-3]}")

@client.event
async def on_ready():
    print("Bot is Happy and Ready!")
    await client.change_presence(activity=discord.Activity(name="Hello World!", type=3))

client.run(os.getenv("TOKEN"))