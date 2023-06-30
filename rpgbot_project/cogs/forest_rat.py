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
    async def encounter_rat(self, ctx):
        enemy_rat = Enemy(name="Rat", max_health=50, current_health=50, attack=5, defense=2, level=1, xp=10)
        player_id = str(ctx.author.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        
        while enemy_rat.current_health > 0 and player.current_health > 0:
            enemy_attack = await sync_to_async(enemy_rat.attack_player)(player)
            player_attack = await sync_to_async(player.attack_enemy)(enemy_rat)
            
            embed = discord.Embed(title="Battle Updates", color=discord.Color.green())
            embed.add_field(name=player.username, value=f":heart: **HP**: {player.current_health}/{player.max_health}\n:crossed_swords: **ATTACK**: {player.attack}\n:shield: **DEFENCE**: {player.defense}", inline=True)
            embed.add_field(name=enemy_rat.name, value=f":heart: **HP**: {enemy_rat.current_health}/{enemy_rat.max_health}\n:crossed_swords: **ATTACK**: {enemy_rat.attack}\n:shield: **DEFENCE**: {enemy_rat.defense}", inline=True)
            embed.add_field(name="Player Attack", value=f"{player.username} attacks {enemy_rat.name} and deals {player_attack} damage.", inline=False)
            embed.add_field(name="Enemy Attack", value=f"{enemy_rat.name} attacks {player.username} and deals {enemy_attack} damage.", inline=False)

            
            message = await ctx.send(embed=embed)
            
            await asyncio.sleep(2)  # Delay for 2 seconds
            
            # Delete previous message
            await message.delete()
        
        if player.current_health > 0:
            victory_embed = discord.Embed(title="Victory!", description=f"You have defeated the {enemy_rat.name}.", color=discord.Color.green())
            await ctx.send(embed=victory_embed)
        else:
            defeat_embed = discord.Embed(title="Defeat!", description="You were defeated in battle. Better luck next time!", color=discord.Color.red())
            await ctx.send(embed=defeat_embed)
