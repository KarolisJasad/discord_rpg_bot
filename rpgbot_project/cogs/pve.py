import discord
from discord.ext import commands

class Enemy:
    def __init__(self, name, hp, attack, defense, magic):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.magic = magic

class Pve(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pve(self, ctx):
        rat = Enemy("Rat", 10, 2, 1, 0)
        bat = Enemy("Bat", 15, 5, 7, 1)
        deer = Enemy("Deer", 30, 9, 4, 3)

        enemy_embed = discord.Embed(
            title="Animals",
            description="Choose an enemy to encounter:",
            color=discord.Color.red()
        )

        enemy_embed.add_field(name=rat.name, value=f"HP: {rat.hp}\nAttack: {rat.attack}\nDefense: {rat.defense}\nMagic: {rat.magic}")
        enemy_embed.add_field(name=bat.name, value=f"HP: {bat.hp}\nAttack: {bat.attack}\nDefense: {bat.defense}\nMagic: {bat.magic}")
        enemy_embed.add_field(name=deer.name, value=f"HP: {deer.hp}\nAttack: {deer.attack}\nDefense: {deer.defense}\nMagic: {deer.magic}")

        await ctx.send(embed=enemy_embed)

def setup(bot):
    bot.add_cog(Pve(bot))