import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Player, ItemInstance
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from collections import Counter


class SelectView(discord.ui.View):
    def __init__(self, inventory_items, *, timeout=180, bot: GameBot):
        self.bot = bot
        super().__init__(timeout=timeout)

        item_counts = Counter(item.item.name for item in inventory_items)
        added_items = set()  # Track the items that have already been added
        options = []

        for item in inventory_items:
            if item_counts[item.item.name] > 1:
                label = f"{item.item.name} x{item_counts[item.item.name]}"
                if item.item.name not in added_items:
                    added_items.add(item.item.name)  # Add the item to the set
                    options.append(discord.SelectOption(label=label, value=str(item.id)))
            else:
                label = item.item.name
                options.append(discord.SelectOption(label=label, value=str(item.id)))

        select = discord.ui.Select(
            placeholder="Select an item to equip",
            max_values=1,
            min_values=1,
            options=options
        )
        select.callback = self.on_select_item
        self.add_item(select)

        back_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Back", custom_id="back_button")
        back_button.callback = self.on_back_button_click
        self.add_item(back_button)

    async def on_select_item(self, interaction: discord.Interaction):
        selected_option = self.children[0].values[0]
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        item_id = int(selected_option)
        item_instance = await sync_to_async(get_object_or_404)(ItemInstance, id=item_id)

        if await sync_to_async(player.can_equip_item)(item_instance):
            await sync_to_async(player.equip_item)(item_instance)
            await interaction.response.edit_message(content=f"Successfully equipped {item_instance.item.name}.")
        else:
            await interaction.response.edit_message(content=f"You cannot equip {item_instance.item.name}.")

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
        await sync_to_async(print)(inventory_items)
        if inventory_items:
            view = SelectView(inventory_items, bot=self.bot)
            await interaction.followup.send("Select an item from your inventory to equip:", view=view)
        else:
            await interaction.followup.send("Your inventory is empty.")


def setup(bot):
    bot.add_cog(Inventory(bot))
