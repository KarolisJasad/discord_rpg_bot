import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

class Inventory(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
    
    @commands.command()
    async def open_inventory(self, interaction: discord.Interaction):
        pass

def setup(bot):
    bot.add_cog(Inventory(bot))