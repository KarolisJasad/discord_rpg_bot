import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player, Enemy
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from cogs.forest_wolf import ForestWolf
from cogs.forest_bear import ForestBear
from cogs.forest_goblin import ForestGoblin

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

        forest_wolf = await sync_to_async(Enemy.objects.get)(name="Forest wolf")
        forest_wolf_level = forest_wolf.level
        forest_wolf_button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label=f"Forest wolf (Level {forest_wolf_level})",
            custom_id="forest_wolf"
        )
        forest_wolf_button.callback = self.on_wolf_button_click

        forest_bear = await sync_to_async(Enemy.objects.get)(name="Forest bear")
        forest_bear_level = forest_bear.level
        forest_bear_button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label=f"Forest bear (Level {forest_bear_level})",
            custom_id="forest_bear"
        )
        forest_bear_button.callback = self.on_bear_button_click

        forest_goblin = await sync_to_async(Enemy.objects.get)(name="Forest goblin")
        forest_goblin_level = forest_goblin.level
        forest_goblin_button = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label=f"Forest goblin (Level {forest_goblin_level})",
            custom_id="forest_goblin"
        )
        forest_goblin_button.callback = self.on_goblin_button_click

        village = discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label="Back to Village",
            custom_id="village"
        )
        village.callback = self.on_village_button_click

        adventure.add_item(forest_goblin_button)
        adventure.add_item(forest_wolf_button)
        adventure.add_item(forest_bear_button)
        adventure.add_item(village)

        await interaction.followup.send(embed=location_embed, view=adventure)
    
    async def on_wolf_button_click(self, interaction: discord.Interaction):
        forest_wolf_cog = self.bot.get_cog("ForestWolf")
        await interaction.response.defer()
        await forest_wolf_cog.encounter_wolf(interaction)
        roles_to_remove = ["Village", "Cave", "Adventure"]
        roles = [discord.utils.get(interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await interaction.user.remove_roles(*roles)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        character_location = await sync_to_async(Location.objects.get)(name="Forest")
        player.location = character_location
        role = discord.utils.get(interaction.guild.roles, name=player.location.name)
        if role:
            await interaction.user.add_roles(role)
        await sync_to_async(player.save)()

    async def on_bear_button_click(self, interaction: discord.Interaction):
        forest_bear_cog = self.bot.get_cog("ForestBear")
        await interaction.response.defer()
        await forest_bear_cog.encounter_bear(interaction)
        roles_to_remove = ["Village", "Cave", "Adventure"]
        roles = [discord.utils.get(interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await interaction.user.remove_roles(*roles)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        character_location = await sync_to_async(Location.objects.get)(name="Forest")
        player.location = character_location
        role = discord.utils.get(interaction.guild.roles, name=player.location.name)
        if role:
            await interaction.user.add_roles(role)
        await sync_to_async(player.save)()

    async def on_goblin_button_click(self, interaction: discord.Interaction):
        forest_goblin_cog = self.bot.get_cog("ForestGoblin")
        await interaction.response.defer()
        await forest_goblin_cog.encounter_goblin(interaction)
        roles_to_remove = ["Village", "Cave", "Adventure"]
        roles = [discord.utils.get(interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await interaction.user.remove_roles(*roles)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        character_location = await sync_to_async(Location.objects.get)(name="Forest")
        player.location = character_location
        role = discord.utils.get(interaction.guild.roles, name=player.location.name)
        if role:
            await interaction.user.add_roles(role)
        await sync_to_async(player.save)()

    async def on_village_button_click(self, interaction: discord.Interaction):
        village_cog = self.bot.get_cog("Village")
        await interaction.response.defer()
        await village_cog.enter_village(interaction)
        roles_to_remove = ["Forest", "Cave", "Adventure"]
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
    bot.add_cog(Adventure(bot))