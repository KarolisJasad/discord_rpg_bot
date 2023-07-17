import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Player, ItemInstance, Item
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404
from collections import Counter

class SelectView(discord.ui.View):
    def __init__(self, inventory_items, bot: GameBot):
        self.bot = bot
        super().__init__()
        item_counts = Counter(item.item.name for item in inventory_items)
        added_items = set()  # Track the items that have already been added
        options = []
        for item in inventory_items:
            sell_price = item.item.price // 2
            label = f"{item.item.name}\nSell Price: {sell_price} gold"
            options.append(discord.SelectOption(label=label, value=str(item.id)))

        select = discord.ui.Select(
            placeholder="Select an item to sell",
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
        await sync_to_async(print)(item_instance)
        sell_price = round(item_instance.item.price / 2) # Calculate the sell price (half of the item's price)
        player.money += sell_price  # Add the sell price to player's money
        await sync_to_async(player.save)()  # Save the player's changes
        await sync_to_async(item_instance.delete)()  # Delete the item from the inventory

        await interaction.response.edit_message(content=f"You sold {item_instance.item.name} for {sell_price} gold.")

    async def on_back_button_click(self, interaction: discord.Interaction):
        village_cog = self.bot.get_cog("Village")
        await interaction.response.defer()
        await village_cog.enter_village(interaction)

class VillageShopSell(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot
    
    @commands.command()
    async def sell_item(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        inventory_items = await sync_to_async(list)(player.get_inventory_items())
        await sync_to_async(print)(inventory_items)
        if inventory_items:
            view = SelectView(inventory_items, bot=self.bot)
            await interaction.followup.send("Select an item to sell:", view=view)
        else:
            await interaction.followup.send("Your inventory is empty.")

def setup(bot):
    bot.add_cog(VillageShopSell(bot))
