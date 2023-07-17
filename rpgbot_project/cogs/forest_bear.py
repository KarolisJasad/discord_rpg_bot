import discord
from discord.ext import commands
from rpgbot.models import Enemy, Player, Location, EnemyInstance
import random
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import asyncio
from utilities.levelup_embed import handle_level_up
from utilities.fighting_logic import perform_attack, create_battle_embed, handle_battle_outcome

class ForestBear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def encounter_bear(self, interaction: discord.Interaction):
        adventure_location = await sync_to_async(Location.objects.get)(name="Adventure")
        forest_bear = await sync_to_async(Enemy.objects.get)(name="Forest bear")
        enemy_bear = EnemyInstance(enemy=forest_bear, current_health=forest_bear.max_health)
        
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        
        async def attack_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id == interaction.user.id:
                enemy_attack, player_block, player_attack, enemy_block = await perform_attack(player, enemy_bear)
                await handle_level_up(player, button_interaction.channel)
                embed = create_battle_embed(player, enemy_bear, player_attack, enemy_attack, player_block, enemy_block)
                await handle_battle_outcome(self.bot, player, enemy_bear, adventure_location, embed, button_interaction, interaction.channel, message)
        
        async def flee_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id == interaction.user.id:
                flee_successful = random.choice([True, False]) 
                if flee_successful:
                    flee_embed = discord.Embed(title="Flee Successful", description="You successfully fled from the enemy!", color=discord.Color.green())
                    flee_view = discord.ui.View()  
                    await button_interaction.response.edit_message(embed=flee_embed, view=flee_view)
                    await asyncio.sleep(2)  
                    village_cog = self.bot.get_cog("Village")
                    await village_cog.enter_village(interaction)
                else:
                    enemy_attack, player_block, player_attack, enemy_block = await perform_attack(player, enemy_bear, player_attempting_flee=True)
                    embed = create_battle_embed(player, enemy_bear, player_attack, enemy_attack, player_block, enemy_block, flee_failed=True)
                    await button_interaction.response.edit_message(embed=embed)
        
        attack_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Attack", custom_id="attack_button")
        attack_button.callback = attack_button_callback
        
        flee_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Flee", custom_id="flee_button")
        flee_button.callback = flee_button_callback
        
        view = discord.ui.View()
        view.add_item(attack_button)
        view.add_item(flee_button)
        
        embed = create_battle_embed(player, enemy_bear)
        message = await interaction.channel.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(ForestBear(bot))
