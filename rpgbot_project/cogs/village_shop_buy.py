import discord
from discord.ext import commands
from utilities.gamebot import GameBot
from rpgbot.models import Shop, Item, Player, ItemInstance
from asgiref.sync import sync_to_async
from django.shortcuts import get_object_or_404


class VillageShopBuy(commands.Cog):
    def __init__(self, bot: GameBot):
        self.bot = bot

    @commands.command()
    async def open_shop(self, interaction: discord.Interaction):
        village_shop = await sync_to_async(Shop.objects.get)(name="Village Shop")
        items = await sync_to_async(list)(village_shop.items.all())
        
        shop_embed = discord.Embed(title="Village Shop", color=discord.Color.blue())
        for i in range(0, len(items), 3):
            item_group = items[i:i + 3]
            item_info = []
            for item in item_group:
                item_info.append(f"**{item.name}**\nPrice: {item.price}\nAttack: {item.attack}\nHealth: {item.health}\nDefense: {item.defense}")
            shop_embed.add_field(name="\u200b", value="\n".join(item_info), inline=True)
        shop = discord.ui.View()
        for item in items:
            button = discord.ui.Button(style=discord.ButtonStyle.primary, label=f"Buy {item.name}", custom_id=f"buy_button_{item.id}")
            button.callback = self.on_buy_button_click
            shop.add_item(button)
        
        back_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Back", custom_id="back_button")
        back_button.callback = self.on_back_button_click
        shop.add_item(back_button)
        await interaction.followup.send(embed=shop_embed, view=shop)

    async def on_buy_button_click(self, interaction: discord.Interaction):
        player_id = str(interaction.user.id)
        player = await sync_to_async(get_object_or_404)(Player, player_id=player_id)
        
        item_id = int(interaction.data["custom_id"].split("_")[-1])
        item = await sync_to_async(get_object_or_404)(Item, id=item_id)
        if item.price > player.money:
            await interaction.response.edit_message(content=f"You don't have enough gold to buy {item.name}.")
            return
        if player.money >= item.price:
            player.money -= item.price
            await sync_to_async(player.save)()
            # Create an ItemInstance and add it to the player's inventory
            item_instance = await sync_to_async(ItemInstance.objects.create)(
                item=item,
                player=player
            )
            await sync_to_async(player.inventory.add)(item_instance)
            await interaction.response.edit_message(content=f"You have successfully bought {item.name}.")
        else:
            await interaction.response.edit_message(content="Error: Insufficient funds.")
            
    async def on_back_button_click(self, interaction: discord.Interaction):
        village_cog = self.bot.get_cog("Village")
        await interaction.response.defer()
        await village_cog.enter_village(interaction)

def setup(bot):
    bot.add_cog(VillageShopBuy(bot))
