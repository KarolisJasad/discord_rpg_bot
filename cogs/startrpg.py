import discord
from discord.ext import commands
from utilities.gamebot import GameBot

class StartRPG(commands.Cog):
    def __init__(self, bot : GameBot):
        self.bot = bot
        self.page_index = 0  # Initialize the page_index variable to 0

    @commands.command()
    async def startrpg(self, ctx):
        warrior_page = discord.Embed(
            title="Warrior Class",
            description="A powerful class specializing in melee combat.",
            color=discord.Color.blue()
        )
        warrior_page.add_field(name="Stats", value="HP: 100\nAttack: 80\nDefense: 70\nMagic: 20")

        rogue_page = discord.Embed(
            title="Rogue Class",
            description="A swift and stealthy class adept at sneaky maneuvers.",
            color=discord.Color.green()
        )
        rogue_page.add_field(name="Stats", value="HP: 70\nAttack: 60\nDefense: 50\nMagic: 40")

        mage_page = discord.Embed(
            title="Mage Class",
            description="A spellcasting class with powerful magical abilities.",
            color=discord.Color.purple()
        )
        mage_page.add_field(name="Stats", value="HP: 50\nAttack: 40\nDefense: 30\nMagic: 100")

        class_embeds = [warrior_page, rogue_page, mage_page]

        def update_class_message():
            return class_embeds[self.page_index]

        class_selection_view = discord.ui.View()
        select_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Select Class")

        async def on_select_button_click(interaction: discord.Interaction):
            if interaction.data["custom_id"] == "previous_button":
                self.page_index = (self.page_index - 1) % len(class_embeds)
            elif interaction.data["custom_id"] == "next_button":
                self.page_index = (self.page_index + 1) % len(class_embeds)

            await interaction.message.edit(embed=class_embeds[self.page_index])

        previous_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Previous", custom_id="previous_button")
        next_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Next", custom_id="next_button")

        previous_button.callback = on_select_button_click
        next_button.callback = on_select_button_click

        class_selection_view.add_item(previous_button)
        class_selection_view.add_item(next_button)
        class_selection_view.add_item(select_button)

        class_selection_message = await ctx.send(embed=update_class_message(), view=class_selection_view)

        def check_class_selection(interaction):
            return interaction.user == ctx.author and interaction.message.id == class_selection_message.id

        try:
            interaction = await self.bot.wait_for("button_click", check=check_class_selection, timeout=60.0)
            selected_class = None

            if interaction.component.label == "Select Class":
                if self.page_index == 0:
                    selected_class = "Warrior"
                elif self.page_index == 1:
                    selected_class = "Rogue"
                elif self.page_index == 2:
                    selected_class = "Mage"

            await interaction.response.send_message(f"You have selected {selected_class} class.")

        except TimeoutError:
            await class_selection_message.delete()
            await ctx.send("Class selection timed out.", delete_after=10)
            return

        await ctx.send(f"Selected class: {selected_class}")
        # Here you can continue with the logic for the selected class

def setup(bot):
    bot.add_cog(StartRPG(bot))