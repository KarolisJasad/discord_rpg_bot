import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from cogs.classmenu import ClassMenu
from cogs.startrpg import UsernameEntry
from cogs.introduction import Introduction
from cogs.area_selection import AreaSelection
from cogs.forest_rat import ForestRat
from cogs.forest_wolf import ForestWolf
from cogs.forest_bear import ForestBear
from cogs.forest_goblin import ForestGoblin
from cogs.cave_troll import CaveTroll
from cogs.village import Village
from cogs.profile import Profile
from cogs.inventory import Inventory
from cogs.adventure import Adventure
from cogs.village_shop import VillageShop
from cogs.village_shop_buy import VillageShopBuy
from cogs.tavern import Tavern

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
    "cogs.introduction",
    "cogs.area_selection",
    "cogs.forest_rat",
    "cogs.forest_wolf",
    "cogs.forest_bear",
    "cogs.forest_goblin",
    "cogs.cave_troll",
    "cogs.village",
    "cogs.profile",
    "cogs.inventory",
    "cogs.adventure",
    "cogs.village_shop",
    "cogs.village_shop_buy",
    "cogs.tavern",

]

bot = GameBot(init_cogs)

@bot.event
async def on_ready():
    print("Bot is online!")
    await bot.add_cog(ClassMenu(bot)) 
    await bot.add_cog(UsernameEntry(bot))
    await bot.add_cog(Introduction(bot))
    await bot.add_cog(AreaSelection(bot))
    await bot.add_cog(ForestRat(bot))
    await bot.add_cog(ForestWolf(bot))
    await bot.add_cog(ForestBear(bot))
    await bot.add_cog(ForestGoblin(bot))
    await bot.add_cog(CaveTroll(bot))
    await bot.add_cog(Village(bot))
    await bot.add_cog(Profile(bot))
    await bot.add_cog(Inventory(bot))
    await bot.add_cog(Adventure(bot))
    await bot.add_cog(VillageShop(bot))
    await bot.add_cog(VillageShopBuy(bot))
    await bot.add_cog(Tavern(bot))

bot.run(TOKEN)