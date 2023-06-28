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
    

pages = [
    {
        'title': "Option 1",
        'description': "This is option 1. Select this to see more information.",
        'details': "More details about option 1."
    },
    {
        'title': "Option 2",
        'description': "This is option 2. Select this to see more information.",
        'details': "More details about option 2."
    },
    {
        'title': "Option 3",
        'description': "This is option 3. Select this to see more information.",
        'details': "More details about option 3."
    }
]

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Information Menu", description=pages[0]['description'])
    embed.set_footer(text=f"Page 1/{len(pages)}")

    message = await ctx.send(embed=embed)

    await message.add_reaction('⬅️')
    await message.add_reaction('1️⃣')
    await message.add_reaction('➡️')
    await message.add_reaction('🔍')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['⬅️', '1️⃣', '➡️', '🔍']

    current_page = 0

    while True:
        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            if str(reaction.emoji) == '⬅️':
                current_page = (current_page - 1) % len(pages)
            elif str(reaction.emoji) == '1️⃣':
                current_page = 0
            elif str(reaction.emoji) == '➡️':
                current_page = (current_page + 1) % len(pages)
            elif str(reaction.emoji) == '🔍':
                await message.delete()
                await show_details(ctx, pages[current_page])

                # Exit the loop after showing the details
                break

            embed.description = pages[current_page]['description']
            embed.set_footer(text=f"Page {current_page+1}/{len(pages)}")
            await message.edit(embed=embed)
            await message.remove_reaction(reaction, ctx.author)
        except TimeoutError:
            break

async def show_details(ctx, page):
    embed = discord.Embed(title=page['title'], description=page['details'])
    await ctx.send(embed=embed)


bot.run(TOKEN)