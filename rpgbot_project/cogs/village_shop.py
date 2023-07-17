import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404


class VillageShop(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
    
    @commands.command()
    async def open_village_shop(self, interaction: discord.Interaction):
        village_shop_location = await sync_to_async(Location.objects.get)(name="Village Shop")
        village_shop_page = discord.Embed(title=village_shop_location.name, color=discord.Color.blue())
        village_shop_page.add_field(name="Description", value=village_shop_location.description)
        village_shop_page.set_image(url="https://i.imgur.com/p0lSGWK.png")
        
        location_embed = village_shop_page
        village = discord.ui.View()
        embed = discord.Embed(title="Village shop", color=discord.Color.green())
        
        buy_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Buy", custom_id="buy_button")
        buy_button.callback = self.on_buy_button_click
        
        sell_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Sell", custom_id="sell_button")
        sell_button.callback = self.on_sell_button_click
        
        back_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Back to the village", custom_id="back_button")
        back_button.callback = self.on_back_button_click
        
        village.add_item(buy_button)
        village.add_item(sell_button)
        village.add_item(back_button)
        await interaction.followup.send(embed=location_embed, view=village)

    async def on_buy_button_click(self, interaction: discord.Interaction):
        village_shop_cog = self.bot.get_cog("VillageShopBuy")
        await interaction.response.defer()
        await village_shop_cog.open_shop(interaction)

    async def on_sell_button_click(self, interaction: discord.Interaction):
        # Handle the sell button click event
        await interaction.response.defer()
        # Your logic for the sell button

    async def on_back_button_click(self, interaction: discord.Interaction):
        village_cog = self.bot.get_cog("Village")
        await interaction.response.defer()
        await village_cog.enter_village(interaction)
        
        roles_to_remove = ["Forest", "Cave", "Adventure", "Village Shop"]
        roles = [discord.utils.get(interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await interaction.user.remove_roles(*roles)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        character_location = await sync_to_async(Location.objects.get)(name="Village")
        player.location = character_location
        role = discord.utils.get(interaction.guild.roles, name=player.location.name)
        if role:
            await interaction.user.add_roles(role)
        await sync_to_async(player.save)()

def setup(bot):
    bot.add_cog(VillageShop(bot))