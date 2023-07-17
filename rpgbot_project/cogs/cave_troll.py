import discord
from discord.ext import commands
from rpgbot.models import Enemy, Player, Location, EnemyInstance
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import asyncio

class CaveTroll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def encounter_troll(self, interaction: discord.Interaction):
        cave_location = await sync_to_async(Location.objects.get)(name="Cave")
        cave_troll = await sync_to_async(Enemy.objects.get)(name="Cave troll")
        enemy_troll = EnemyInstance(enemy=cave_troll, current_health=cave_troll.max_health)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)

        def check_author(author_id):
            return interaction.user.id == author_id

        async def attack_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id == interaction.user.id:
                # Player's attack logic goes here
                enemy_attack, player_block = await sync_to_async(enemy_troll.attack_player)(player)
                player_attack, enemy_block = await sync_to_async(player.attack_enemy)(enemy_troll)

                embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
                embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
                embed.add_field(name=enemy_troll.enemy.name, value=f":heart: **HP**: {enemy_troll.current_health}/{enemy_troll.enemy.max_health}\n:crossed_swords: **ATTACK**: {enemy_troll.enemy.attack}\n:shield: **DEFENCE**: {enemy_troll.enemy.defense}", inline=True)
                embed.add_field(name="Player Attack", value=f"{player.username} attacks {enemy_troll.enemy.name} and deals {player_attack} damage {enemy_block} was blocked.", inline=False)
                embed.add_field(name="Enemy Attack", value=f"{enemy_troll.enemy.name} attacks {player.username} and deals {enemy_attack} damage {player_block} was blocked.", inline=False)

                if player.current_health > 0 and enemy_troll.current_health <= 0:
                    victory_embed = discord.Embed(title="Victory", description=f"{player.username} defeated {enemy_troll.enemy.name}, you've gained {enemy_troll.enemy.xp} exeprience and {enemy_troll.enemy.gold} gold!", color=discord.Color.green())
                    victory_embed.add_field(name="Journey continues", value=cave_location.victory_message)
                    victory_embed.set_image(url="https://i.imgur.com/SfgZiYt.jpg")
                    continue_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Continue", custom_id="continue_button")
                    view.add_item(continue_button)
                    await interaction.channel.send(embed=victory_embed)
                elif player.current_health <= 0 and enemy_troll.current_health > 0:
                    defeat_embed = discord.Embed(title="Defeat", description=f"{player.username} was defeated by {enemy_troll.enemy.name}!", color=discord.Color.red())
                    defeat_embed.add_field(name="Journey ended", value=cave_location.defeat_message)
                    defeat_embed.set_image(url="https://i.imgur.com/ZTgj0so.jpg")
                    roles_to_remove = ["Forest", "Village", "Cave", "Warrior", "Mage", "Rogue"]
                    roles = [discord.utils.get(button_interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
                    roles = [role for role in roles if role is not None]  # Filter out None values
                    if roles:
                        await button_interaction.user.remove_roles(*roles)
                    await interaction.channel.send(embed=defeat_embed)

                await button_interaction.response.edit_message(embed=embed)     

        # Create the attack button
        attack_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Attack", custom_id="attack_button")
        attack_button.callback = attack_button_callback

        view = discord.ui.View()
        view.add_item(attack_button)

        embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
        embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
        embed.add_field(name=enemy_troll.enemy.name, value=f":heart: **HP**: {enemy_troll.current_health}/{enemy_troll.enemy.max_health}\n:crossed_swords: **ATTACK**: {enemy_troll.enemy.attack}\n:shield: **DEFENCE**: {enemy_troll.enemy.defense}", inline=True)
        embed.add_field(name="Player Attack", value="Waiting for your next move...", inline=False)
        embed.add_field(name="Enemy Attack", value="Responding to your action", inline=False)

        message = await interaction.channel.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(CaveTroll(bot))
