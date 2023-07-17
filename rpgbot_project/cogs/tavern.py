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
        
        tavern_embed.add_field(name="Bartender", value=story, inline=False)

        talk_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Talk to bartender", custom_id="talk")
        talk_button.callback = self.talk_to_bartender

        tavern_view = discord.ui.View()
        tavern_view.add_item(talk_button)

        await interaction.followup.send(embed=tavern_embed, view=tavern_view)

    async def talk_to_bartender(self, interaction: discord.Interaction):
        await interaction.response.defer()

        tavern_embed = discord.Embed(title="Tavern", color=discord.Color.purple())
        tavern_embed.set_image(url="https://i.imgur.com/pYEHZoA.jpg")
        tavern_embed.add_field(name="Bartender", value="It's a terrible time. A fearsome troll has been terrorizing the nearby villages, leaving destruction in its wake.")
        
        talk_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Is there anything we can do to stop the troll?", custom_id="talk2")
        talk_button.callback = self.talk_to_bartender2

        tavern_view = discord.ui.View()
        tavern_view.add_item(talk_button)
        
        await interaction.followup.send(embed=tavern_embed, view=tavern_view)

    async def talk_to_bartender2(self, interaction: discord.Interaction):
        await interaction.response.defer()

        tavern_embed = discord.Embed(title="Tavern", color=discord.Color.purple())
        tavern_embed.set_image(url="https://i.imgur.com/pYEHZoA.jpg")
        tavern_embed.add_field(name="Bartender", value="There might be a way. The legendary sword of the ancients is said to have the power to vanquish the troll. But it's hidden deep within the ancient forest, guarded by dangerous creatures.")
            
        talk_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="I'am going to retrieve the sword but now I need to regain my strength", custom_id="talk3")

        tavern_view = discord.ui.View()
        tavern_view.add_item(talk_button)
        
        await interaction.followup.send(embed=tavern_embed, view=tavern_view)

    async def talk_to_bartender3(self, interaction: discord.Interaction):
        await interaction.response.defer()

        tavern_embed = discord.Embed(title="Tavern", color=discord.Color.purple())
        tavern_embed.set_image(url="https://i.imgur.com/pYEHZoA.jpg")
        tavern_embed.add_field(name="Bartender", value="Of course. Allow me to restore your hit points, brave adventurer.")
        
        tavern_view = discord.ui.View()
        
        await self.regenerate_hp(interaction)  # Call the regenerate_hp method to restore hit points
        
        await interaction.followup.send(embed=tavern_embed, view=tavern_view)

    async def regenerate_hp(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        
        # Regenerate hit points
        player.hit_points = player.max_hit_points
        await sync_to_async(player.save)()
        
        await interaction.followup.send(content="Your hit points have been fully regenerated.")

def setup(bot):
    bot.add_cog(Tavern(bot))
