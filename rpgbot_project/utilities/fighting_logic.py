from rpgbot.models import EnemyInstance
from asgiref.sync import sync_to_async
from utilities.levelup_embed import handle_level_up
import discord
import asyncio

async def perform_attack(player, enemy, player_attempting_flee=False):
    enemy_attack, player_block = await sync_to_async(enemy.attack_player)(player)
    
    if not player_attempting_flee:
        player_attack, enemy_block = await sync_to_async(player.attack_enemy)(enemy)
    else:
        player_attack, enemy_block = None, None
    
    return enemy_attack, player_block, player_attack, enemy_block

def create_battle_embed(player, enemy, player_attack=None, enemy_attack=None, player_block=None, enemy_block=None, flee_failed=False):
    embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
    embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
    embed.add_field(name=enemy.enemy.name, value=f":heart: **HP**: {enemy.current_health}/{enemy.enemy.max_health}\n:crossed_swords: **ATTACK**: {enemy.enemy.attack}\n:shield: **DEFENCE**: {enemy.enemy.defense}", inline=True)
    
    if flee_failed:
        embed.add_field(name="Player action", value="You failed to flee from the enemy!", inline=False)
        embed.add_field(name="Enemy Attack", value=f"{enemy.enemy.name} attacks {player.username} and deals {enemy_attack} damage {player_block} was blocked.", inline=False)
    elif player_attack is not None and enemy_attack is not None:
        embed.add_field(name="Player Attack", value=f"{player.username} attacks {enemy.enemy.name} and deals {player_attack} damage {enemy_block} was blocked.", inline=False)
        embed.add_field(name="Enemy Attack", value=f"{enemy.enemy.name} attacks {player.username} and deals {enemy_attack} damage {player_block} was blocked.", inline=False)
    else:
        embed.add_field(name="Player Attack", value="Waiting for your next move...", inline=False)
        embed.add_field(name="Enemy Attack", value="Responding to your action", inline=False)
    
    return embed

def create_victory_embed(player, enemy):
    victory_embed = discord.Embed(title="Victory", description=f"{player.username} defeated {enemy.enemy.name}, you've gained {enemy.enemy.xp} experience and {enemy.enemy.gold} gold!", color=discord.Color.green())
    victory_embed.add_field(name="Journey continues", value="Choose your next option")
    victory_embed.set_image(url="https://i.imgur.com/SfgZiYt.jpg")
    
    return victory_embed

def create_defeat_embed(player, enemy):
    defeat_embed = discord.Embed(title="Defeat", description=f"{player.username} was defeated by {enemy.enemy.name}!", color=discord.Color.red())
    defeat_embed.add_field(name="Journey ended", value="You've lost to a formidabble opponent, unfortunately your journey ends.")
    defeat_embed.set_image(url="https://i.imgur.com/ZTgj0so.jpg")
    
    return defeat_embed

async def handle_battle_outcome(bot, player, enemy, location, embed, button_interaction, channel, message):
    async def continue_button_click(interaction: discord.Interaction):
        if interaction.data["custom_id"] == "continue_button":
            role = discord.utils.get(interaction.user.guild.roles, name="Forest")
            if role:
                await interaction.user.remove_roles(role)
            role = discord.utils.get(interaction.user.guild.roles, name="Village")
            if role:
                await interaction.user.add_roles(role)
            await interaction.response.defer()
            village_cog = bot.get_cog("Village")
            await village_cog.enter_village(interaction)

    async def adventure_button_click(interaction: discord.Interaction):
        adventure_cog = bot.get_cog("Adventure")
        await interaction.response.defer()
        role = discord.utils.get(interaction.user.guild.roles, name="Adventure")
        if role:
            await interaction.user.add_roles(role)
        roles_to_remove = ["Village", "Forest"]
        roles = [discord.utils.get(interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await interaction.user.remove_roles(*roles)
        await adventure_cog.open_adventure(interaction)

    if player.current_health > 0 and enemy.current_health <= 0:
        victory_embed = create_victory_embed(player, enemy)
        continue_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Enter village", custom_id="continue_button")
        victory_view = discord.ui.View()
        victory_view.add_item(continue_button)
        continue_button.callback = continue_button_click

        adventure_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Adventure", custom_id="adventure_button")
        victory_view.add_item(adventure_button)
        adventure_button.callback = adventure_button_click

        await button_interaction.response.edit_message(embed=embed, view=None)
        await channel.send(embed=victory_embed, view=victory_view)
        await message.delete()
    elif player.current_health <= 0 and enemy.current_health >= 0:
        defeat_embed = create_defeat_embed(player, enemy)
        roles_to_remove = ["Forest", "Village", "Cave", "Warrior", "Mage", "Rogue"]
        roles = [discord.utils.get(button_interaction.user.guild.roles, name=role_name) for role_name in roles_to_remove]
        roles = [role for role in roles if role is not None]  # Filter out None values
        if roles:
            await button_interaction.user.remove_roles(*roles)
        await channel.send(embed=defeat_embed)
    else:
        await button_interaction.response.edit_message(embed=embed)
