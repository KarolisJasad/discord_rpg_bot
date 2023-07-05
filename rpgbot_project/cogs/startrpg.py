import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from .classmenu import ClassMenu
from rpgbot.models import Player
from asgiref.sync import sync_to_async

class UsernameEntry(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot

    @commands.command()
    async def startrpg(self, ctx):
        def check_author(m):
            return m.author == ctx.author

        player = await sync_to_async(Player.objects.filter(player_id=ctx.author.id).exists)()

        if player:
            # Player entry exists, redirect to the associated channel
            player = await sync_to_async(Player.objects.get)(player_id=ctx.author.id)
            channel_name = f"rpg-channel-{player.username.lower()}"
            existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)

            if existing_channel:
                # Update ctx with the existing channel
                ctx.channel = existing_channel
                class_menu_command = self.bot.get_command("classmenu")
                await ctx.invoke(class_menu_command)
                return

        else:
            await ctx.send("Please enter your username.")
            try:
                username_msg = await self.bot.wait_for("message", check=check_author, timeout=60.0)
                username = username_msg.content

                channel_name = f"RPG-Channel-{username}"
                existing_channel = discord.utils.get(ctx.guild.channels, name=channel_name)

                if existing_channel:
                    ctx.channel = existing_channel  # Update ctx with the existing channel
                else:
                    overwrites = {
                        ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        ctx.author: discord.PermissionOverwrite(read_messages=True)
                    }
                    channel = await ctx.guild.create_text_channel(channel_name, overwrites=overwrites)
                    ctx.channel = channel  # Update ctx with the new channel
                    print(channel.id)

                await sync_to_async(Player.objects.create)(player_id=ctx.author.id, discord_name=ctx.author.name, username=username)
                await ctx.send(f"Welcome, {username}!")

                # Proceed to the class menu
                class_menu_command = self.bot.get_command("classmenu")
                await ctx.invoke(class_menu_command)

            except:
                await ctx.send("Username entry timed out.", delete_after=10)
                return

def setup(bot):
    bot.add_cog(UsernameEntry(bot))
