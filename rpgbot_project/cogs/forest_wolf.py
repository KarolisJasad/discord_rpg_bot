import discord
from discord.ext import commands
from rpgbot.models import Enemy, Player, Location, EnemyInstance
import random
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
import asyncio
from utilities.levelup_embed import handle_level_up
from utilities.fighting_logic import perform_attack, create_battle_embed, handle_battle_outcome

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
        
        async def attack_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id == interaction.user.id:
                # Call the perform_attack function from fighting_logic.py
                enemy_attack, player_block, player_attack, enemy_block = await perform_attack(player, enemy_wolf)
                await handle_level_up(player, button_interaction.channel)
                embed = create_battle_embed(player, enemy_wolf, player_attack, enemy_attack, player_block, enemy_block)
                await handle_battle_outcome(self.bot, player, enemy_wolf, forest_location, embed, button_interaction, interaction.channel, message)
        async def flee_button_callback(button_interaction: discord.Interaction):
            if button_interaction.user.id == interaction.user.id:
                flee_successful = random.choice([True, False])  # 50/50 chance of success
                if flee_successful:
                    flee_embed = discord.Embed(title="Flee Successful", description="You successfully fled from the enemy!", color=discord.Color.green())
                    flee_view = discord.ui.View()  # Create a new view without buttons
                    await button_interaction.response.edit_message(embed=flee_embed, view=flee_view)
                    # Add a delay before returning to the village
                    await asyncio.sleep(2)  # Adjust the delay time as needed
                    village_cog = self.bot.get_cog("Village")
                    await village_cog.enter_village(interaction)
                else:
                    enemy_attack, player_block, player_attack, enemy_block = await perform_attack(player, enemy_wolf, player_attempting_flee=True)
                    embed = create_battle_embed(player, enemy_wolf, player_attack, enemy_attack, player_block, enemy_block, flee_failed=True)
                    await button_interaction.response.edit_message(embed=embed)
        
        attack_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Attack", custom_id="attack_button")
        attack_button.callback = attack_button_callback
        
        flee_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Flee", custom_id="flee_button")
        flee_button.callback = flee_button_callback
        
        view = discord.ui.View()
        view.add_item(attack_button)
        view.add_item(flee_button)
        embed = create_battle_embed(player, enemy_wolf)
        message = await interaction.channel.send(embed=embed, view=view)

def setup(bot):
    bot.add_cog(ForestWolf(bot))
