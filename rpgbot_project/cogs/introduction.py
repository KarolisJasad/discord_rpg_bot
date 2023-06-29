import discord
from discord.ext import commands


class Introduction(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def introduction(self, ctx):
        introductory_embed = discord.Embed(
            title="Welcome to the Adventure!",
            description="You wake up in a mysterious place with two paths ahead of you. Where would you like to go?",
            color=discord.Color.gold()
        )
        introductory_embed.set_thumbnail(url="https://i.imgur.com/4iY6fcm.png")

        view = discord.ui.View()

        async def on_forest_button_click(interaction: discord.Interaction):
            await interaction.response.send_message("You decided to go to the Forest!", ephemeral=True)
            # Implement the logic for the Forest path

        async def on_cave_button_click(interaction: discord.Interaction):
            await interaction.response.send_message("You decided to go to the Cave!", ephemeral=True)
            # Implement the logic for the Cave path

        forest_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Forest", custom_id="forest_button")
        cave_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Cave", custom_id="cave_button")

        forest_button.callback = on_forest_button_click
        cave_button.callback = on_cave_button_click

        view.add_item(forest_button)
        view.add_item(cave_button)

        await ctx.send(embed=introductory_embed, view=view)


def setup(bot):
    bot.add_cog(Introduction(bot))
