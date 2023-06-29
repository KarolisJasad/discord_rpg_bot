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

    @commands.command()
    async def classmenu(self, ctx):
        warrior_page = discord.Embed(
            title="Choose your class!",
            color=discord.Color.blue()
        )
        warrior_page.add_field(name="Warrior", value="A powerful class specializing in melee combat.")
        warrior_page.add_field(name="Stats", value="HP: 100\nAttack: 80\nDefense: 70\nMagic: 20")
        warrior_image = discord.File("media/class_images/Warrior.jpg", filename="Warrior.jpg")
        warrior_page.set_image(url="attachment://Warrior.jpg")
        
        rogue_page = discord.Embed(
            title="Choose your class!",
            color=discord.Color.green()
        )
        rogue_page.add_field(name="Rogue", value="A swift and stealthy class adept at sneaky maneuvers.")
        rogue_page.add_field(name="Stats", value="HP: 70\nAttack: 60\nDefense: 50\nMagic: 40")
        rogue_image = discord.File("media/class_images/Rogue.png", filename="Rogue.png")
        rogue_page.set_image(url="attachment://Rogue.png")

        mage_page = discord.Embed(
            title="Choose your class!",
            color=discord.Color.purple()
        )
        mage_page.add_field(name="Mage", value="A spellcasting class with powerful magical abilities.")
        mage_page.add_field(name="Stats", value="HP: 50\nAttack: 40\nDefense: 30\nMagic: 100")
        mage_image = discord.File("media/class_images/Mage.png", filename="Mage.png")
        mage_page.set_image(url="attachment://Mage.png")

        class_embeds = [warrior_page, rogue_page, mage_page]
        class_images = [warrior_image, rogue_image, mage_image]

        def update_class_message():
            return class_embeds[self.page_index]
        
        class_selection_view = discord.ui.View()
        select_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Select Class")

        async def on_select_button_click(interaction: discord.Interaction):
            if interaction.data["custom_id"] == "previous_button":
                self.page_index = (self.page_index - 1) % len(class_embeds)
            elif interaction.data["custom_id"] == "next_button":
                self.page_index = (self.page_index + 1) % len(class_embeds)
            elif interaction.data["custom_id"] == "select_button":
                print("Selected button")
                await sync_to_async(self.handle_class_selection(interaction))

            await interaction.message.edit(embed=class_embeds[self.page_index])

        previous_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Previous", custom_id="previous_button")
        next_button = discord.ui.Button(style=discord.ButtonStyle.secondary, label="Next", custom_id="next_button")
        select_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Select Class", custom_id="select_button")

        previous_button.callback = on_select_button_click
        next_button.callback = on_select_button_click
        select_button.callback = on_select_button_click

        class_selection_view.add_item(previous_button)
        class_selection_view.add_item(next_button)
        class_selection_view.add_item(select_button)

        await ctx.send(file=class_images[self.page_index], embed=class_embeds[self.page_index], view=class_selection_view)

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
        player = await sync_to_async(get_object_or_404(Player, player_id=player_id))
        player.character_class = selected_class
        await player.save()

        await interaction.response.send_message(f"You have selected {selected_class} class.")

def setup(bot):
    bot.add_cog(ClassMenu(bot))