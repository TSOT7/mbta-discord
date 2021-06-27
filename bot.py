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
    if line in ('Fairmount','Fitchburg','Worcester','Franklin','Greenbush','Haverhill','Kingston','Lowell','Middleborough','Needham','Newburyport','Providence'):
        line = "CR-" + line
    data = requests.get("https://api-v3.mbta.com/routes/" + line).json()
    stops = requests.get("https://api-v3.mbta.com/stops?filter[route]=" + line).json()
    termini = data['data']['attributes']['direction_destinations']
    direction = data['data']['attributes']['direction_names']
    color = int(data['data']['attributes']['color'], 16)
    a = []
    for stop in stops['data']:
        a.append(stop.get('attributes').get('name'))
    zipped = list(zip(termini, direction))
    test = zipped[0][0] + " ("+zipped[0][1]+ ")\n" + zipped[1][0] + " ("+zipped[1][1]+")"
    embedVar = discord.Embed(title= line, description="Info for " + line + " line", color=color)
    embedVar.add_field(name="Termini", value= test, inline=False)
    embedVar.add_field(name="Stops", value="\n".join(a), inline=False)
    await ctx.send(embed=embedVar)

@bot.command()
async def getlines(ctx):
    big_list = (getLinesFunc())
    embedVar = discord.Embed(title="MBTA Lines", description="All MBTA transportation lines", color=6750873)
    embedVar.add_field(name="Commuter Rail", value=big_list[0], inline=False)
    embedVar.add_field(name="Metro", value=big_list[1], inline=False)
    embedVar.add_field(name="Bus", value=big_list[2], inline=False)
    await ctx.send(embed=embedVar)


@bot.command()
async def commands(ctx):
    embedVar = discord.Embed(title="Commands", description="List of all commands", color=6750873)
    embedVar.add_field(name="info + [line name]", value="Command to get info about a specific line (Commuter Rail + Metro)", inline=False)
    embedVar.add_field(name="getlines", value="Get a list of all Commuter Rail, Metro, and Buses", inline=False)
    embedVar.add_field(name="commands", value="Get a list of all commands", inline=False)
    await ctx.send(embed=embedVar)

bot.run('')