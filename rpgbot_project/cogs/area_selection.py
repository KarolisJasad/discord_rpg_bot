import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404


class AreaSelection(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
        self.page_index = 0  # Initialize the page_index variable to 0
        self.previous_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Previous", custom_id="previous_button")
        self.next_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Next", custom_id="next_button")
        self.select_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Select Location", custom_id="select_button")
        self.forest_rat_cog = None
        self.cave_troll_cog = None

    @commands.command()
    async def areaselection(self, ctx):
        forest_location = await sync_to_async(Location.objects.get)(name="Forest")
        cave_location = await sync_to_async(Location.objects.get)(name="Cave")
        village_location = await sync_to_async(Location.objects.get)(name="Village")

        forest_page = discord.Embed(title=forest_location.name, color=discord.Color.blue())
        forest_page.add_field(name="Description", value=forest_location.description)
        forest_page.set_image(url="https://i.imgur.com/ogmBOx9.jpg")

        cave_page = discord.Embed(title=cave_location.name, color=discord.Color.blue())
        cave_page.add_field(name="Description", value=cave_location.description)
        cave_page.set_image(url="https://i.imgur.com/kcMI7hi.jpg")

        village_page = discord.Embed(title=village_location.name, color=discord.Color.blue())
        village_page.add_field(name="Description", value=village_location.description)
        village_page.set_image(url="https://i.imgur.com/ciYuIoa.jpg")

        location_embeds = [forest_page, cave_page, village_page]

        location_selection_view = discord.ui.View()

        async def on_select_button_click(interaction: discord.Interaction):
            await interaction.response.defer()
            
            if interaction.data["custom_id"] == "previous_button":
                self.page_index = (self.page_index - 1) % len(location_embeds)
            elif interaction.data["custom_id"] == "next_button":
                self.page_index = (self.page_index + 1) % len(location_embeds)
            elif interaction.data["custom_id"] == "select_button":
                await self.page_navigation(interaction, location_embeds)

            await interaction.message.edit(embed=location_embeds[self.page_index])

        self.previous_button.callback = on_select_button_click
        self.next_button.callback = on_select_button_click
        self.select_button.callback = on_select_button_click

        location_selection_view.add_item(self.previous_button)
        location_selection_view.add_item(self.next_button)
        location_selection_view.add_item(self.select_button)

        self.forest_rat_cog = self.bot.get_cog("ForestRat")
        self.cave_troll_cog = self.bot.get_cog("CaveTroll")
        self.village_cog = self.bot.get_cog("Village")
        
        await ctx.send(embed=location_embeds[self.page_index], view=location_selection_view)

    async def page_navigation(self, interaction, location_embeds):
        await interaction.message.delete()
        await interaction.channel.send(f"You have selected {location_embeds[self.page_index].title}")
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        character_location = await sync_to_async(Location.objects.get)(name=location_embeds[self.page_index].title)
        player.location = character_location
        role = discord.utils.get(interaction.guild.roles, name=player.location.name)
        if role:
            await interaction.user.add_roles(role)
        await sync_to_async(player.save)()

        if self.page_index == 0:
            await self.forest_rat_cog.encounter_rat(interaction)
        elif self.page_index == 1:
            await self.cave_troll_cog.encounter_troll(interaction)


def setup(bot):
    bot.add_cog(AreaSelection(bot))
