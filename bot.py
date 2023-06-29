import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class SimpleView(discord.ui.View):
    @discord.ui.button(label="Hello", style=discord.ButtonStyle.blurple)
    async def hello(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("World")

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    general_channel = discord.utils.get(guild.channels, name="general")
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    print("Member list:")
    for member in guild.members:
        print(member.name)

    await general_channel.send("I'm online now!")

@bot.command()
async def button(ctx):
    view = SimpleView()
    await ctx.send(view=view)

@bot.command()
async def startrpg(ctx):
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

    message = await ctx.send(embed=class_embeds[0])
    page_index = 0

    # Add reactions for navigation
    await message.add_reaction('⬅️')
    await message.add_reaction('➡️')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️']

    while True:
        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check)

            if str(reaction.emoji) == '➡️':
                page_index = (page_index + 1) % len(class_embeds)
            elif str(reaction.emoji) == '⬅️':
                page_index = (page_index - 1) % len(class_embeds)

            await message.edit(embed=class_embeds[page_index])
            await message.remove_reaction(reaction, ctx.author)

        except TimeoutError:
            await message.delete()
            break

    select_button = discord.ui.Button(style=discord.ButtonStyle.primary, label="Select Class")

    class_selection_view = discord.ui.View()
    class_selection_view.add_item(select_button)

    class_selection_message = await ctx.send("Select your class:", view=class_selection_view)

    def check_class_selection(interaction):
        return interaction.user == ctx.author and interaction.message.id == class_selection_message.id

    try:
        interaction = await bot.wait_for("button_click", check=check_class_selection, timeout=60.0)
        selected_class = None

        if interaction.component.label == "Select Class":
            if page_index == 0:
                selected_class = "Warrior"
            elif page_index == 1:
                selected_class = "Rogue"
            elif page_index == 2:
                selected_class = "Mage"

        await interaction.response.send_message(f"You have selected {selected_class} class.")

    except TimeoutError:
        await class_selection_message.delete()
        await ctx.send("Class selection timed out.", delete_after=10)
        return

    await ctx.send(f"Selected class: {selected_class}")
    # Here you can continue with the logic for the selected class

bot.run(TOKEN)