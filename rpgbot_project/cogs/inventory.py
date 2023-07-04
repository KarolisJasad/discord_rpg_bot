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
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        
        inventory_page = discord.Embed(title="Inventory", color=discord.Color.dark_green())
        equipped_items = await sync_to_async(player.get_equipped_items)()
        print(equipped_items)
        inventory_items = await sync_to_async(player.get_inventory_items)()

def setup(bot):
    bot.add_cog(Inventory(bot))