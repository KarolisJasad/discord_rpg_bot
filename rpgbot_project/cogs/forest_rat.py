import discord
from discord.ext import commands
from rpgbot.models import Enemy, Player, Location
import random
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import asyncio

class ForestRat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def encounter_rat(self, interaction: discord.Interaction):
        forest_location = await sync_to_async(Location.objects.get)(name="Forest")
        enemy_rat = Enemy(name="Rat", max_health=50, current_health=50, attack=5, defense=2, level=1, gold=5, xp=10)
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

                if player.current_health > 0 and enemy_rat.current_health <= 0:
                    victory_embed = discord.Embed(title="Victory", description=f"{player.username} defeated {enemy_rat.name}, you've gained {enemy_rat.xp} exeprience and {enemy_rat.gold} gold!", color=discord.Color.green())
                    victory_embed.add_field(name="Journey continues", value=forest_location.victory_message)
                    victory_embed.set_image(url="https://i.imgur.com/SfgZiYt.jpg")
                    continue_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Enter village", custom_id="continue_button")
                    victory_view = discord.ui.View()
                    victory_view.add_item(continue_button)    
                elif player.current_health <= 0 and enemy_rat.current_health > 0:
                    defeat_embed = discord.Embed(title="Defeat", description=f"{player.username} was defeated by {enemy_rat.name}!", color=discord.Color.red())
                    defeat_embed.add_field(name="Journey ended", value=forest_location.defeat_message)
                    defeat_embed.set_image(url="https://i.imgur.com/ZTgj0so.jpg")
                

                
                if player.current_health > 0 and enemy_rat.current_health <= 0:
                    await button_interaction.response.edit_message(embed=embed)
                    await interaction.channel.send(embed=victory_embed, view=victory_view)
                elif player.current_health <= 0 and enemy_rat.current_health >= 0:
                    await interaction.channel.send(embed=defeat_embed)
                else:
                    await button_interaction.response.edit_message(embed=embed)

        # Create the attack button
        attack_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Attack", custom_id="attack_button")
        attack_button.callback = attack_button_callback

        view = discord.ui.View()
        view.add_item(attack_button)

        embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
        embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
        embed.add_field(name=enemy_rat.name, value=f":heart: **HP**: {enemy_rat.current_health}/{enemy_rat.max_health}\n:crossed_swords: **ATTACK**: {enemy_rat.attack}\n:shield: **DEFENCE**: {enemy_rat.defense}", inline=True)
        embed.add_field(name="Player Attack", value="Waiting for your next move...", inline=False)
        embed.add_field(name="Enemy Attack", value="Responding to your action", inline=False)

        message = await interaction.channel.send(embed=embed, view=view)

        # Wait for the button click event or timeout after 180 seconds
        try:
            await asyncio.wait_for(view.wait(), timeout=180.0)
        except asyncio.TimeoutError:
            await interaction.channel.send("Battle timeout. You took too long to respond.")
            return

def setup(bot):
    bot.add_cog(ForestRat(bot))
