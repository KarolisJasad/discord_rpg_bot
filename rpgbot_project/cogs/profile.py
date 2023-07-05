import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

class Profile(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
    
    @commands.command()
    async def open_profile(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        equipped_items = await sync_to_async(player.get_equipped_items)()

        profile_embed = discord.Embed(title="Player Profile", color=discord.Color.dark_blue())
        profile_embed.add_field(name="Player stats", value=f'Health: {player.current_health}/{player.max_health}\nPlayer attack: {player.attack}\nPlayer defense: {player.defense}', inline=False)
        
        if equipped_items:
            equipped_items_str = "\n".join([f"{item.type}: {item.name}" for item in equipped_items])
            profile_embed.add_field(name="Equipped items", value=equipped_items_str, inline=False)
        else:
            profile_embed.add_field(name="Equipped items", value="No items equipped", inline=False)

        profile_page = discord.ui.View()
        inventory_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Inventory", custom_id="inventory_button")
        inventory_button.callback = self.on_inventory_button_click
        profile_page.add_item(inventory_button)

        await interaction.followup.send(embed=profile_embed, view=profile_page)
    
    async def on_inventory_button_click(self, interaction: discord.Interaction):
        self.inventory_cog = self.bot.get_cog("Inventory")
        await interaction.response.defer()
        await self.inventory_cog.open_inventory(interaction)

def setup(bot):
    bot.add_cog(Profile(bot))
