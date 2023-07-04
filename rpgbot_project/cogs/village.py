import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404


class Village(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot

    @commands.command()
    async def enter_village(self, interaction: discord.Interaction):
        village_location = await sync_to_async(Location.objects.get)(name="Village")
        village_page = discord.Embed(title=village_location.name, color=discord.Color.blue())
        village_page.add_field(name="Description", value=village_location.description)
        village_page.set_image(url="https://i.imgur.com/ciYuIoa.jpg")

        location_embed = village_page

        village = discord.ui.View()
        inventory_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Inventory", custom_id="inventory_button")
        inventory_button.callback = self.on_inventory_button_click
        shop_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Visit Shop", custom_id="shop_button")
        shop_button.callback = self.on_shop_button_click
        village.add_item(inventory_button)
        village.add_item(shop_button)


        await interaction.followup.send(embed=location_embed, view=village)

    async def on_shop_button_click(self, interaction: discord.Interaction):
        self.shop_cog = self.bot.get_cog("ShopCog")
        await interaction.response.defer()
        await self.shop_cog.open_shop(interaction)

    async def on_inventory_button_click(self, interaction: discord.Interaction):
        self.inventory_cog = self.bot.get_cog("Inventory")
        await interaction.response.defer()
        await self.inventory_cog.open_inventory(interaction)
        
def setup(bot):
    bot.add_cog(Village(bot))