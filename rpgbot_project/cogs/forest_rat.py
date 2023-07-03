import discord
from discord.ext import commands
from rpgbot.models import Enemy, Player
import random
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import asyncio

class ForestRat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def encounter_rat(self, interaction: discord.Interaction):
        enemy_rat = Enemy(name="Rat", max_health=50, current_health=50, attack=5, defense=2, level=1, xp=10)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)

        def check_author(author_id):
            return interaction.user.id == author_id

        async def attack_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id == interaction.user.id:
                # Player's attack logic goes here
                enemy_attack = await sync_to_async(enemy_rat.attack_player)(player)
                player_attack = await sync_to_async(player.attack_enemy)(enemy_rat)
                
                embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
                embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
                embed.add_field(name=enemy_rat.name, value=f":heart: **HP**: {enemy_rat.current_health}/{enemy_rat.max_health}\n:crossed_swords: **ATTACK**: {enemy_rat.attack}\n:shield: **DEFENCE**: {enemy_rat.defense}", inline=True)
                embed.add_field(name="Player Attack", value=f"{player.username} attacks {enemy_rat.name} and deals {player_attack} damage.", inline=False)
                embed.add_field(name="Enemy Attack", value=f"{enemy_rat.name} attacks {player.username} and deals {enemy_attack} damage.", inline=False)

                await button_interaction.response.edit_message(embed=embed)
        
        # Create the attack button
        attack_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Attack", custom_id="attack_button")
        view = discord.ui.View()
        view.add_item(attack_button)

        embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
        embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
        embed.add_field(name=enemy_rat.name, value=f":heart: **HP**: {enemy_rat.current_health}/{enemy_rat.max_health}\n:crossed_swords: **ATTACK**: {enemy_rat.attack}\n:shield: **DEFENCE**: {enemy_rat.defense}", inline=True)
        embed.add_field(name="Player Attack", value="Waiting for your next move...", inline=False)
        embed.add_field(name="Enemy Attack", value="Responding to your action", inline=False)

        message = await interaction.channel.send(embed=embed, view=view)

        try:
            button_interaction = await self.bot.wait_for("button_click", check=check_author, timeout=180.0)
            if button_interaction.component.custom_id == "attack_button":
                await attack_button_callback(button_interaction)
            else:
                # Handle other buttons if needed
                pass
        except asyncio.TimeoutError:
            pass

        if player.current_health > 0:
            victory_embed = discord.Embed(title="Victory!", description=f"You have defeated the {enemy_rat.name}.", color=discord.Color.green())
            await interaction.channel.send(embed=victory_embed)
        else:
            defeat_embed = discord.Embed(title="Defeat!", description="You were defeated in battle. Better luck next time!", color=discord.Color.red())
            await interaction.channel.send(embed=defeat_embed)

        await message.delete()


def setup(bot):
    bot.add_cog(ForestRat(bot))