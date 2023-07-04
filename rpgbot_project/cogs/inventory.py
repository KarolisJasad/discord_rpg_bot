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
        equipped_items = await sync_to_async(player.get_equipped_items)()
        inventory_items = await sync_to_async(player.get_inventory_items)()


        inventory_page = discord.Embed(title="Equipped items", color=discord.Color.dark_green())
        for item in equipped_items:
            inventory_page.add_field(name=item.type, value=item.name)
        inventory_embed = inventory_page
        inventory = discord.ui.View()
        await interaction.followup.send(embed=inventory_embed, view=inventory)

def setup(bot):
    bot.add_cog(Inventory(bot))