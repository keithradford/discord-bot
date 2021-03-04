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

@bot.command(name='clan', help='Fetches clan data.')
async def get_cwl(ctx):
    c = clash.Clan()
    data = c.clan_info()
    message = '**Level ' + str(data['level']) + ' | ' + data['league'] + ' | ' + str(data['members']) + ' members**\n\n' + data['desc']
    embed = discord.Embed(title=data['name'], description=message, color=0xd12600, inline=False)
    embed.set_thumbnail(url = data['image'])

    await ctx.send(embed=embed)

@bot.command(name='cwl', help='Prints data related to the Clan War League.')
async def get_cwl(ctx, *args):
    c = clash.Clan()
    s = ' '
    if len(args) >= 1:
        message = c.cwl_clan_info(s.join(args))
    else:
        message = c.cwl_info()

    embed = discord.Embed(title="Clan War League", description=message, color=0x004080, inline=False)
    embed.set_thumbnail(url = "https://static.wikia.nocookie.net/clashofclans/images/c/c0/War_League_Main_Banner.png/revision/latest/scale-to-width-down/340?cb=20181023145516")
    await ctx.send(embed=embed)

@bot.command(name='moist', help='Picks the moist member of the day.')
async def get_cwl(ctx):
    c = clash.Clan()
    message = c.get_random_member()
    await ctx.send(message)

@bot.command(name='bob', help='bob')
async def bob(ctx):
    await ctx.send('bob')

@bot.command(name='dam', help='nico')
async def dam(ctx):
    await ctx.send('<:nico:717580375844454490>')

@bot.command(name='member', help="Fetches stats for a user in the clan.")
async def get_member(ctx, name):
    c = clash.Clan()
    s = ' '
    if len(args) >= 1:
        data = c.get_member(s.join(args))
    else:
        data = c.get_member(name)
    embed = discord.Embed(title=data['name'], description=data['message'], color=0x9900d1, inline=False)
    embed.set_thumbnail(url = data['image'])
    await ctx.send(embed=embed)

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