import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Player, Item
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404


class Select(discord.ui.Select):
    def __init__(self, inventory_items):
        options = [
            discord.SelectOption(label=item.name, value=str(item.id))
            for item in inventory_items
        ]
        super().__init__(
            placeholder="Select an item to equip",
            max_values=1,
            min_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        selected_option = self.values[0]
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        item_id = int(selected_option)
        item = await sync_to_async(get_object_or_404)(Item, id=item_id)

        if await sync_to_async(player.can_equip_item)(item):
            await sync_to_async(player.equip_item)(item)
            await interaction.response.edit_message(content=f"Successfully equipped {item.name}.")
        else:
            await interaction.response.edit_message(content=f"You cannot equip {item.name}.")


class SelectView(discord.ui.View):
    def __init__(self, inventory_items, *, timeout=180, bot: GameBot):
        self.bot = bot
        super().__init__(timeout=timeout)
        self.add_item(Select(inventory_items))
        back_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Back", custom_id="back_button")
        back_button.callback = self.on_back_button_click
        self.add_item(back_button)

    async def on_back_button_click(self, interaction: discord.Interaction):
        self.profile_cog = self.bot.get_cog("Profile")
        await interaction.response.defer()
        await self.profile_cog.open_profile(interaction)


class Inventory(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot

    @commands.command()
    async def open_inventory(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        inventory_items = await sync_to_async(list)(player.get_inventory_items())

        if inventory_items:
            view = SelectView(inventory_items, bot=self.bot)
            await interaction.followup.send("Select an item from your inventory to equip:", view=view)
        else:
            await interaction.followup.send("Your inventory is empty.")


def setup(bot):
    bot.add_cog(Inventory(bot))
