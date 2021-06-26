import discord
from discord.ext import commands
import requests
import json

description = "Basic bot used to connect to MBTA."

bot = commands.Bot(command_prefix='mbta!', description=description)

def getLinesFunc():
    lines = requests.get("https://api-v3.mbta.com/routes/")
    linesJson = lines.json()
    commuter_rail = []
    metro = []
    bus = []
    for line in linesJson['data']:
        if line.get("attributes").get("description") == "Commuter Rail":
            commuter_rail.append(line.get("attributes").get("long_name"))
        elif line.get("attributes").get("description") == "Rapid Transit":
            metro.append(line.get("attributes").get("long_name"))
        elif line.get("attributes").get("description") == "Key Bus":
            bus.append(line.get("attributes").get("long_name"))
    print(linesJson['data'])
    commuter_rail = "\n".join(commuter_rail)
    metro = "\n".join(metro)
    bus = "\n".join(bus)
    return [commuter_rail,metro,bus]

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
    test = "Termini: " + zipped[0][0] + " ("+zipped[0][1]+ "), " + zipped[1][0] + " ("+zipped[1][1]+")"
    await ctx.send(test)

@bot.command()
async def getlines(ctx):
    big_list = (getLinesFunc())
    embedVar = discord.Embed(title="MBTA Lines", description="All MBTA transportation lines", color=0x00ff00)
    embedVar.add_field(name="Commuter Rail", value=big_list[0], inline=False)
    embedVar.add_field(name="Metro", value=big_list[1], inline=False)
    embedVar.add_field(name="Bus", value=big_list[2], inline=False)
    await ctx.send(embed=embedVar)


bot.run('')