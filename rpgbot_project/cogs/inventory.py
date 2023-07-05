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
        inventory_items = await sync_to_async(list)(player.get_inventory_items())

        inventory_embed = discord.Embed(title="Inventory", color=discord.Color.dark_green())
        if inventory_items:
            for item in inventory_items:
                inventory_embed.add_field(name=item.type, value=item.name, inline=False)
        else:
            inventory_embed.add_field(name="No items", value="Your inventory is empty.")
        
        inventory_view = discord.ui.View()
        await interaction.followup.send(embed=inventory_embed, view=inventory_view)

def setup(bot):
    bot.add_cog(Inventory(bot))
