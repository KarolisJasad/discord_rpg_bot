import discord
from asgiref.sync import sync_to_async

async def handle_level_up(player, channel):
    if await sync_to_async(player.increase_level)():
        level_up_embed = discord.Embed(
            title="Level Up!",
            description=f"Congratulations, {player.username}! You have reached level {player.level}!",
            color=discord.Color.green()
        )
        level_up_embed.add_field(name="New Abilities", value="You have gained new abilities and stat improvements.", inline=False)
        
        await channel.send(embed=level_up_embed)