import discord
from discord.ext import commands
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rpgbot_project.settings")
django.setup()

class GameBot(commands.Bot):
    def __init__(self, cogs: list):
        self.init_cogs = cogs
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True

        super().__init__(command_prefix='!', intents=intents)

    async def setup_cogs(self):
        for cog in self.init_cogs:
            try:
                self.load_extension(cog)
                print(f"Loaded cog {cog}.")
            except Exception as e:
                print(f"Failed to load cog {cog}. Error: {str(e)}.")

    async def on_ready(self):
        print("Bot is online.")

    def setup(self, bot):
        self.bot = bot