import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404


class Village(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
        self.shop_items = ["Sword", "Armor", "Health Potion"]
        self.shop_cog = None

    @commands.command()
    async def enter_village(self, interaction: discord.Interaction):
        village_location = await sync_to_async(Location.objects.get)(name="Village")
        village_page = discord.Embed(title=village_location.name, color=discord.Color.blue())
        village_page.add_field(name="Description", value=village_location.description)
        village_page.set_image(url="https://i.imgur.com/ciYuIoa.jpg")

        location_embed = village_page

        location_selection_view = discord.ui.View()
        shop_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Visit Shop", custom_id="shop_button")
        shop_button.callback = self.on_shop_button_click
        location_selection_view.add_item(shop_button)

        self.shop_cog = self.bot.get_cog("ShopCog")

        await interaction.followup.send(embed=location_embed, view=location_selection_view)

    async def on_shop_button_click(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.shop_cog.open_shop(interaction)

def setup(bot):
    bot.add_cog(Village(bot))