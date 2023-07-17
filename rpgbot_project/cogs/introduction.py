import discord
from discord.ext import commands
from rpgbot.models import Player
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from utilities.gamebot import GameBot


class Introduction(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot

    @commands.command()
    async def introduction(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        
        introductory_embed = discord.Embed(
            title=f"Welcome to the Adventure {player.username}!",
            description="You wake up in the middle of nowhere, surrounded by a dense mist. As you regain your senses, you notice two distinct paths stretching out before you, each shrouded in mystery and uncertainty. Looks like one path is leading to a forest while the other path is leading towards a cave",
            color=discord.Color.gold()
        )
        introductory_embed.set_thumbnail(url="https://i.imgur.com/4iY6fcm.png")
        view = discord.ui.View()
        
        async def on_continue_button_click(interaction: discord.Interaction):
            await interaction.response.send_message("You've decided to continue your journey", ephemeral=True)
            await interaction.message.delete()
            area_selection_cog = self.bot.get_cog("AreaSelection")
            await area_selection_cog.areaselection(interaction.channel)
        
        continue_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Continue", custom_id="continue_button")
        continue_button.callback = on_continue_button_click
        
        view.add_item(continue_button)
        await interaction.followup.send(embed=introductory_embed, view=view)

def setup(bot):
    bot.add_cog(Introduction(bot))