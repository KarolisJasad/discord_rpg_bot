import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from cogs.forest_rat import ForestRat
from cogs.forest_wolf import ForestWolf
from cogs.forest_bear import ForestBear

class Adventure(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
    
    @commands.command()
    async def open_adventure(self, interaction: discord.Interaction):
        adventure_location = await sync_to_async(Location.objects.get)(name="Adventure")
        adventure_page = discord.Embed(title=adventure_location.name, color=discord.Color.blue())
        adventure_page.add_field(name="Description", value=adventure_location.description)
        adventure_page.set_image(url="https://i.imgur.com/fAkBSje.png")

        location_embed = adventure_page

        adventure = discord.ui.View()
        forest_rat = discord.ui.Button(style=discord.ButtonStyle.primary, label="Forest rat", custom_id="forest_rat")
        forest_rat.callback = self.on_rat_button_click
        forest_wolf = discord.ui.Button(style=discord.ButtonStyle.primary, label="Forest wolf", custom_id="forest_wolf")
        forest_wolf.callback = self.on_wolf_button_click
        forest_bear = discord.ui.Button(style=discord.ButtonStyle.primary, label="Forest bear", custom_id="forest_bear")
        forest_bear.callback = self.on_bear_button_click
        village = discord.ui.Button(style=discord.ButtonStyle.primary, label="Back to Village", custom_id="village")
        village.callback = self.on_village_button_click
        adventure.add_item(forest_rat)
        adventure.add_item(forest_wolf)
        adventure.add_item(forest_bear)
        adventure.add_item(village)

        await interaction.followup.send(embed=location_embed, view=adventure)

    async def on_rat_button_click(self, interaction: discord.Interaction):
        forest_rat_cog = self.bot.get_cog("ForestRat")
        await interaction.response.defer()
        await forest_rat_cog.encounter_rat(interaction)
    
    async def on_wolf_button_click(self, interaction: discord.Interaction):
        forest_wolf_cog = self.bot.get_cog("ForestWolf")
        await interaction.response.defer()
        await forest_wolf_cog.encounter_wolf(interaction)

    async def on_bear_button_click(self, interaction: discord.Interaction):
        forest_bear_cog = self.bot.get_cog("ForestBear")
        await interaction.response.defer()
        await forest_bear_cog.encounter_bear(interaction)

    async def on_village_button_click(self, interaction: discord.Interaction):
        village_cog = self.bot.get_cog("Village")
        await interaction.response.defer()
        await village_cog.enter_village(interaction)

def setup(bot):
    bot.add_cog(Adventure(bot))

