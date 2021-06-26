import discord
from discord.ext import commands
import requests
import json

description = "Basic bot used to connect to MBTA."

bot = commands.Bot(command_prefix='mbta!', description=description)

def getLinesFunc():
    lines = requests.get("https://api-v3.mbta.com/lines/?include=routes")
    linesJson = lines.json()
    lineNames = []
    for line in linesJson['data']:
        lineNames.append(line.get("id"))
    print(linesJson['data'])
    return lineNames

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def info(ctx, line):
    data = requests.get("https://api-v3.mbta.com/routes/" + line).json()
    termini = data['data']['attributes']['direction_destinations']
    direction = data['data']['attributes']['direction_names']
    zipped = list(zip(termini, direction))
    print(zipped)
    test = "Termini: " + zipped[0][0] + " ("+zipped[0][1]+ ")" + ", " + zipped[1][0] + " ("+zipped[1][1]+")"
    await ctx.send(test)

@bot.command()
async def getlines(ctx):
    await ctx.send(getLinesFunc())

    #
    # embedVar = discord.Embed(title="MBTA Lines", description="All MBTA rail lines", color=0x00ff00)
    # embedVar.add_field(name="", value="hi", inline=False)
    # embedVar.add_field(name="Field2", value="hi2", inline=False)
    # await ctx.send(embed=embedVar)

# @bot.command()
# async def update:


bot.run('')