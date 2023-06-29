import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Player, CharacterClass
from django.shortcuts import get_object_or_404
from asgiref.sync import sync_to_async
from urllib.parse import urlparse


class ClassMenu(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
        self.page_index = 0  # Initialize the page_index variable to 0
        self.previous_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Previous",
                                                 custom_id="previous_button")
        self.next_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Next", custom_id="next_button")
        self.select_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Select Class",
                                               custom_id="select_button")

    @commands.command()
    async def classmenu(self, ctx):
        warrior_page = discord.Embed(
            title="Choose your class!",
            color=discord.Color.blue()
        )
        warrior_page.add_field(name="Warrior", value="A powerful class specializing in melee combat.")
        warrior_page.add_field(name="Stats", value="HP: 100\nAttack: 80\nDefense: 70\nMagic: 20")
        warrior_page.set_image(url="https://i.imgur.com/gC1E7oa.gif")

        rogue_page = discord.Embed(
            title="Choose your class!",
            color=discord.Color.green()
        )
        rogue_page.add_field(name="Rogue", value="A swift and stealthy class adept at sneaky maneuvers.")
        rogue_page.add_field(name="Stats", value="HP: 70\nAttack: 60\nDefense: 50\nMagic: 40")
        rogue_page.set_image(url="https://i.imgur.com/CEeh45e.gif")

        mage_page = discord.Embed(
            title="Choose your class!"
            color=discord.Color.purple()
        )
        mage_page.add_field(name="Mage", value="A spellcasting class with powerful magical abilities.")
        mage_page.add_field(name="Stats", value="HP: 50\nAttack: 40\nDefense: 30\nMagic: 100")
        mage_page.set_image(url="https://i.imgur.com/CI9x4fc.gif")

        class_embeds = [warrior_page, rogue_page, mage_page]

        class_selection_view = discord.ui.View()

        async def on_select_button_click(interaction: discord.Interaction):
            if interaction.data["custom_id"] == "previous_button":
                self.page_index = (self.page_index - 1) % len(class_embeds)
                print(self.page_index)
                await interaction.response.defer()
            elif interaction.data["custom_id"] == "next_button":
                self.page_index = (self.page_index + 1) % len(class_embeds)
                await interaction.response.defer()
            elif interaction.data["custom_id"] == "select_button":
                print("Selected button")
                await self.handle_class_selection(interaction)
                await interaction.response.defer()

            await interaction.message.edit(embed=class_embeds[self.page_index])

        self.previous_button.callback = on_select_button_click
        self.next_button.callback = on_select_button_click
        self.select_button.callback = on_select_button_click

        class_selection_view.add_item(self.previous_button)
        class_selection_view.add_item(self.next_button)
        class_selection_view.add_item(self.select_button)

        await ctx.send(embed=class_embeds[self.page_index], view=class_selection_view)

    async def handle_class_selection(self, interaction):
        print("Working function")
        selected_class = None

        if self.page_index == 0:
            selected_class = "Warrior"
        elif self.page_index == 1:
            selected_class = "Rogue"
        elif self.page_index == 2:
            selected_class = "Mage"

        print(selected_class)
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)

        # Retrieve the currently browsed character class
        character_class = await sync_to_async(CharacterClass.objects.get)(class_type=selected_class)

        # Update the player's character_class field
        player.character_class = character_class

        # Update player's stats based on the selected class
        player.max_health = character_class.health
        player.current_health = character_class.health
        player.attack = character_class.attack
        player.defense = character_class.defense

        await sync_to_async(player.save)()

        await interaction.response.send_message(f"You have selected {selected_class} class.")

        await interaction.message.delete()

def setup(bot):
    bot.add_cog(ClassMenu(bot))
