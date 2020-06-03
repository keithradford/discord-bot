# bot.py
import os
import discord
from discord.ext import commands
import random
import clash

TOKEN = os.environ.get('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='member', help="Fetches stats for a user in the clan.")
async def get_member(ctx, name):
    try:
        c = clash.Clan()
        message = c.get_member(name)
        await ctx.send(message)
    except commands.errors.MissingRequiredArgument:
        await ctx.send('Member name required: **!member <name>**')

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice:int, number_of_sides:int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

bot.run(TOKEN)