'''
bot.py
Runs the Discord bot.
Creates the commands and their actions that users can call the bot upon.
'''

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

@bot.command(name='cwl', help='Prints data related to the Clan War League.')
async def get_cwl(ctx, *args):
    c = clash.Clan()
    message = c.cwl_info()
    s = ' '
    if len(args) >= 1:
        message = c.cwl_clan_info(s.join(args))
    await ctx.send(message)

@bot.command(name='moist', help='Picks the moist member of the day.')
async def get_cwl(ctx):
    c = clash.Clan()
    message = c.get_random_member()
    await ctx.send(message)

@bot.command(name='bob', help='bob')
async def bob(ctx):
    await ctx.send('bob')

@bot.command(name='member', help="Fetches stats for a user in the clan.")
async def get_member(ctx, name):
    c = clash.Clan()
    message = c.get_member(name)
    await ctx.send(message)

@bot.command(name='war', help="Fetches the clan's war state.")
async def get_war(ctx):
    c = clash.Clan()
    message = c.get_war()
    await ctx.send(message)

@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice:int, number_of_sides:int):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


bot.run(TOKEN)