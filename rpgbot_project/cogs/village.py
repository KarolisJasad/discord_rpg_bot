import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from cogs.village_shop import Village_shop


class Village(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot

    @commands.command()
    async def enter_village(self, interaction: discord.Interaction):
        roles_to_remove = ["Forest", "Cave", "Adventure"]
        roles = [discord.utils.get(interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await interaction.user.remove_roles(*roles)
        village_location = await sync_to_async(Location.objects.get)(name="Village")
        village_page = discord.Embed(title=village_location.name, color=discord.Color.blue())
        village_page.add_field(name="Description", value=village_location.description)
        village_page.set_image(url="https://i.imgur.com/ciYuIoa.jpg")

        location_embed = village_page

        village = discord.ui.View()
        shop_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Visit Shop", custom_id="shop_button")
        shop_button.callback = self.on_shop_button_click
        profile_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Profile", custom_id="profile_button")
        profile_button.callback = self.on_profile_button_click
        adventure_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Adventure", custom_id="adventure_button")
        adventure_button.callback = self.on_adventure_button_click
        village.add_item(shop_button)
        village.add_item(profile_button)
        village.add_item(adventure_button)

        await interaction.followup.send(embed=location_embed, view=village)

    async def on_shop_button_click(self, interaction: discord.Interaction):
        self.shop_cog = self.bot.get_cog("Village_shop")
        await interaction.response.defer()
        roles_to_remove = ["Forest", "Cave", "Adventure", "Village"]
        roles = [discord.utils.get(interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await interaction.user.remove_roles(*roles)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        character_location = await sync_to_async(Location.objects.get)(name="Village Shop")
        player.location = character_location
        role = discord.utils.get(interaction.guild.roles, name=player.location.name)
        if role:
            await interaction.user.add_roles(role)
        await sync_to_async(player.save)()
        await self.shop_cog.open_village_shop(interaction)
    
    async def on_profile_button_click(self, interaction: discord.Interaction):
        self.profile_cog = self.bot.get_cog("Profile")
        await interaction.response.defer()
        await self.profile_cog.open_profile(interaction)

    async def on_adventure_button_click(self, interaction: discord.Interaction):
        self.adventure_cog = self.bot.get_cog("Adventure")
        await interaction.response.defer()
        roles_to_remove = ["Forest", "Village", "Cave"]
        roles = [discord.utils.get(interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await interaction.user.remove_roles(*roles)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        character_location = await sync_to_async(Location.objects.get)(name="Adventure")
        player.location = character_location
        role = discord.utils.get(interaction.guild.roles, name=player.location.name)
        if role:
            await interaction.user.add_roles(role)
        await sync_to_async(player.save)()
        await self.adventure_cog.open_adventure(interaction)

def setup(bot):
    bot.add_cog(Village(bot))