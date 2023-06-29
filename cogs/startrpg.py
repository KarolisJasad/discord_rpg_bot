import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from .classmenu import ClassMenu

class UsernameEntry(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot

    @commands.command()
    async def startrpg(self, ctx):
        def check_author(m):
            return m.author == ctx.author

        await ctx.send("Please enter your username.")

        try:
            username_msg = await self.bot.wait_for("message", check=check_author, timeout=60.0)
            username = username_msg.content

            await ctx.send(f"Welcome, {username}!")

            # Proceed to the class menu
            class_menu_command = self.bot.get_command("classmenu")
            await ctx.invoke(class_menu_command)

        except:
            await ctx.send("Username entry timed out.", delete_after=10)
            return

def setup(bot):
    bot.add_cog(UsernameEntry(bot))