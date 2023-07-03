import discord
from discord.ext import commands
from rpgbot.models import Enemy, Player, Location
import random
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import asyncio

class CaveTroll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def encounter_troll(self, interaction: discord.Interaction):
        cave_location = await sync_to_async(Location.objects.get)(name="Cave")
        enemy_troll = Enemy(name="Troll", max_health=500, current_health=500, attack=100, defense=10, level=1, gold=500, xp=100)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)

        def check_author(author_id):
            return interaction.user.id == author_id

        async def attack_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id == interaction.user.id:
                # Player's attack logic goes here
                enemy_attack = await sync_to_async(enemy_troll.attack_player)(player)
                player_attack = await sync_to_async(player.attack_enemy)(enemy_troll)

                embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
                embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
                embed.add_field(name=enemy_troll.name, value=f":heart: **HP**: {enemy_troll.current_health}/{enemy_troll.max_health}\n:crossed_swords: **ATTACK**: {enemy_troll.attack}\n:shield: **DEFENCE**: {enemy_troll.defense}", inline=True)
                embed.add_field(name="Player Attack", value=f"{player.username} attacks {enemy_troll.name} and deals {player_attack} damage.", inline=False)
                embed.add_field(name="Enemy Attack", value=f"{enemy_troll.name} attacks {player.username} and deals {enemy_attack} damage.", inline=False)

                if player.current_health > 0 and enemy_troll.current_health <= 0:
                    victory_embed = discord.Embed(title="Victory", description=f"{player.username} defeated {enemy_troll.name}, you've gained {enemy_troll.xp} exeprience and {enemy_troll.gold} gold!", color=discord.Color.green())
                    victory_embed.add_field(name="Journey continues", value=cave_location.victory_message)
                    victory_embed.set_image(url="https://i.imgur.com/SfgZiYt.jpg")
                    continue_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Continue", custom_id="continue_button")
                    view.add_item(continue_button)
                    await interaction.channel.send(embed=victory_embed)
                elif player.current_health <= 0 and enemy_troll.current_health > 0:
                    defeat_embed = discord.Embed(title="Defeat", description=f"{player.username} was defeated by {enemy_troll.name}!", color=discord.Color.red())
                    defeat_embed.add_field(name="Journey ended", value=cave_location.defeat_message)
                    defeat_embed.set_image(url="https://i.imgur.com/ZTgj0so.jpg")
                    await interaction.channel.send(embed=defeat_embed)

                await button_interaction.response.edit_message(embed=embed)
                

        # Create the attack button
        attack_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Attack", custom_id="attack_button")
        attack_button.callback = attack_button_callback

        view = discord.ui.View()
        view.add_item(attack_button)

        embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
        embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
        embed.add_field(name=enemy_troll.name, value=f":heart: **HP**: {enemy_troll.current_health}/{enemy_troll.max_health}\n:crossed_swords: **ATTACK**: {enemy_troll.attack}\n:shield: **DEFENCE**: {enemy_troll.defense}", inline=True)
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
    bot.add_cog(CaveTroll(bot))
