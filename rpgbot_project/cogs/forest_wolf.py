import discord
from discord.ext import commands
from rpgbot.models import Enemy, Player, Location, EnemyInstance
import random
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import asyncio
from utilities.levelup_embed import handle_level_up
from cogs.village import Village

class ForestWolf(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def encounter_wolf(self, interaction: discord.Interaction):
        forest_location = await sync_to_async(Location.objects.get)(name="Forest")
        forest_wolf = await sync_to_async(Enemy.objects.get)(name="Forest wolf")
        enemy_wolf = EnemyInstance(enemy=forest_wolf, current_health=forest_wolf.max_health)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)

        def check_author(author_id):
            return interaction.user.id == author_id

        async def attack_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id == interaction.user.id:
                # Player's attack logic goes here
                enemy_attack, player_block = await sync_to_async(enemy_wolf.attack_player)(player)
                player_attack, enemy_block = await sync_to_async(player.attack_enemy)(enemy_wolf)

                await handle_level_up(player, button_interaction.channel)

                embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
                embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
                embed.add_field(name=enemy_wolf.enemy.name, value=f":heart: **HP**: {enemy_wolf.current_health}/{enemy_wolf.enemy.max_health}\n:crossed_swords: **ATTACK**: {enemy_wolf.enemy.attack}\n:shield: **DEFENCE**: {enemy_wolf.enemy.defense}", inline=True)
                embed.add_field(name="Player Attack", value=f"{player.username} attacks {enemy_wolf.enemy.name} and deals {player_attack} damage {enemy_block} was blocked.", inline=False)
                embed.add_field(name="Enemy Attack", value=f"{enemy_wolf.enemy.name} attacks {player.username} and deals {enemy_attack} damage {player_block} was blocked.", inline=False)
                if player.current_health > 0 and enemy_wolf.current_health <= 0:
                    victory_embed = discord.Embed(title="Victory", description=f"{player.username} defeated {enemy_wolf.enemy.name}, you've gained {enemy_wolf.enemy.xp} experience and {enemy_wolf.enemy.gold} gold!", color=discord.Color.green())
                    victory_embed.add_field(name="Journey continues", value=forest_location.victory_message)
                    victory_embed.set_image(url="https://i.imgur.com/SfgZiYt.jpg")
                    continue_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Enter village", custom_id="continue_button")
                    victory_view = discord.ui.View()
                    victory_view.add_item(continue_button)
                    continue_button.callback = continue_button_click
                    adventure_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Adventure", custom_id="adventure_button")
                    victory_view.add_item(adventure_button)
                    adventure_button.callback = on_adventure_button_click
                elif player.current_health <= 0 and enemy_wolf.current_health >= 0:
                    defeat_embed = discord.Embed(title="Defeat", description=f"{player.username} was defeated by {enemy_wolf.enemy.name}!", color=discord.Color.red())
                    defeat_embed.add_field(name="Journey ended", value=forest_location.defeat_message)
                    defeat_embed.set_image(url="https://i.imgur.com/ZTgj0so.jpg")
                    roles_to_remove = ["Forest", "Village", "Cave", "Warrior", "Mage", "Rogue"]
                    roles = [discord.utils.get(button_interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
                    roles = [role for role in roles if role is not None]  # Filter out None values
                    if roles:
                        await button_interaction.user.remove_roles(*roles)
                    await interaction.channel.send(embed=defeat_embed)
                if player.current_health > 0 and enemy_wolf.current_health <= 0:
                    await button_interaction.response.edit_message(embed=embed)
                    await interaction.channel.send(embed=victory_embed, view=victory_view)
                    await message.delete()

                else:
                    await button_interaction.response.edit_message(embed=embed)
        
        async def continue_button_click(interaction: discord.Interaction):
            if interaction.data["custom_id"] == "continue_button":
                role = discord.utils.get(interaction.user.guild.roles, name="Forest")
                if role:
                    await interaction.user.remove_roles(role)
                role = discord.utils.get(interaction.user.guild.roles, name="Village")
                if role:
                    await interaction.user.add_roles(role)
                await interaction.response.defer()
                village_cog = self.bot.get_cog("Village")
                await village_cog.enter_village(interaction)
        
        async def on_adventure_button_click(interaction: discord.Interaction):
            adventure_cog = self.bot.get_cog("Adventure")
            await interaction.response.defer()
            await adventure_cog.open_adventure(interaction)
                
        # Create the attack button
        attack_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Attack", custom_id="attack_button")
        attack_button.callback = attack_button_callback

        view = discord.ui.View()
        view.add_item(attack_button)

        embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
        embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
        embed.add_field(name=enemy_wolf.enemy.name, value=f":heart: **HP**: {enemy_wolf.current_health}/{enemy_wolf.enemy.max_health}\n:crossed_swords: **ATTACK**: {enemy_wolf.enemy.attack}\n:shield: **DEFENCE**: {enemy_wolf.enemy.defense}", inline=True)
        embed.add_field(name="Player Attack", value="Waiting for your next move...", inline=False)
        embed.add_field(name="Enemy Attack", value="Responding to your action", inline=False)

        message = await interaction.channel.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(ForestWolf(bot))
