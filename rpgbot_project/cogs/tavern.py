import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Location, Player
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404

class Tavern(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
    
    @commands.command()
    async def enter_tavern(self, interaction: discord.Interaction):
        tavern_location = await sync_to_async(Location.objects.get)(name="Tavern")
        tavern_embed = discord.Embed(title=tavern_location.name, color=discord.Color.purple())
        tavern_embed.add_field(name="Description", value=tavern_location.description)
        tavern_embed.set_image(url="https://i.imgur.com/pYEHZoA.jpg")

        story = "Welcome to the tavern, weary traveler. Have a seat and rest your bones.\n"
        
        tavern_embed.add_field(name="Tavern", value=story, inline=False)

        talk_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Talk to bard", custom_id="bard")
        talk_button.callback = self.talk_to_bard
        heal_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Talk to bartender", custom_id="bartender")
        heal_button.callback = self.regenerate_hp
        village_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Back to Village", custom_id="village")
        village_button.callback = self.on_village_button_click

        tavern_view = discord.ui.View()
        tavern_view.add_item(talk_button)
        tavern_view.add_item(heal_button)
        tavern_view.add_item(village_button)

        await interaction.followup.send(embed=tavern_embed, view=tavern_view)

    async def talk_to_bard(self, interaction: discord.Interaction):
        await interaction.response.defer()

        tavern_embed = discord.Embed(title="Tavern", color=discord.Color.purple())
        tavern_embed.set_image(url="https://i.imgur.com/pYEHZoA.jpg")
        tavern_embed.add_field(name="Bard", value="It's a terrible time. A fearsome troll has been terrorizing the nearby villages, leaving destruction in its wake.")
        
        talk_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Is there anything we can do to stop the troll?", custom_id="talk2")
        talk_button.callback = self.talk_to_bard2

        tavern_view = discord.ui.View()
        tavern_view.add_item(talk_button)
        
        await interaction.followup.send(embed=tavern_embed, view=tavern_view)

    async def talk_to_bard2(self, interaction: discord.Interaction):
        await interaction.response.defer()

        tavern_embed = discord.Embed(title="Tavern", color=discord.Color.purple())
        tavern_embed.set_image(url="https://i.imgur.com/pYEHZoA.jpg")
        tavern_embed.add_field(name="Bard", value="There might be a way. The legendary sword of the ancients is said to have the power to vanquish the troll. But it's hidden deep within the ancient forest, guarded by dangerous creatures.")
        
        talk_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="I'm going to retrieve the sword but now I need to regain my strength", custom_id="talk3")
        talk_button.callback = self.talk_to_bard3

        tavern_view = discord.ui.View()
        tavern_view.add_item(talk_button)
        
        await interaction.followup.send(embed=tavern_embed, view=tavern_view)

    async def talk_to_bard3(self, interaction: discord.Interaction):
        await interaction.response.defer()
        tavern_embed = discord.Embed(title="Tavern", color=discord.Color.purple())
        tavern_embed.set_image(url="https://i.imgur.com/pYEHZoA.jpg")
        tavern_embed.add_field(name="Bard", value="Thank you for your help, brave adventurer!")
        village_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Back to Village", custom_id="village")
        village_button.callback = self.on_village_button_click

        tavern_view = discord.ui.View()
        tavern_view.add_item(village_button)
        
        await interaction.followup.send(embed=tavern_embed, view=tavern_view)

    async def regenerate_hp(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        player.current_health = player.max_health
        await interaction.response.edit_message(content=f"You feel fresh and strong again.")
        await sync_to_async(player.save)()

    async def on_village_button_click(self, interaction: discord.Interaction):
        village_cog = self.bot.get_cog("Village")
        await interaction.response.defer()
        await village_cog.enter_village(interaction)
        roles_to_remove = ["Forest", "Cave", "Adventure", "Tavern", "Village Shop"]
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
    bot.add_cog(Tavern(bot))
