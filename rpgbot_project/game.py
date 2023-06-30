import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from cogs.classmenu import ClassMenu
from cogs.startrpg import UsernameEntry
from cogs.pve import Pve
from cogs.introduction import Introduction
from cogs.area_selection import AreaSelection
from cogs.forest_rat import ForestRat


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Load Cogs
init_cogs = [
    "cogs.classmenu",
    "cogs.startrpg",
    "cogs.pve",
    "cogs.introduction",
    "cogs.area_selection"
    'cogs.forest_rat'
]

bot = GameBot(init_cogs)

@bot.event
async def on_ready():
    print("Bot is online.")
    await bot.add_cog(ClassMenu(bot)) 
    await bot.add_cog(UsernameEntry(bot))
    await bot.add_cog(Pve(bot))
    await bot.add_cog(Introduction(bot))
    await bot.add_cog(AreaSelection(bot))
    await bot.add_cog(ForestRat(bot))

# Add the ClassMenu cog to the bot
bot.run(TOKEN)