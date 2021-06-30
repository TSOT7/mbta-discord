import discord
from discord.ext import commands
import requests
import time
import json
description = "Basic bot used to connect to MBTA."
bot = commands.Bot(command_prefix='mbta!', description=description, help_command=None)
def getLinesFunc():
    lines = requests.get("https://api-v3.mbta.com/routes/")
    linesJson = lines.json()
    commuter_rail = []
    metro = []
    bus = []
    for line in linesJson['data']:
        if line.get("attributes").get("description") == "Commuter Rail":
            commuter_rail.append(line.get("attributes").get("long_name") + " (ID: " + line.get("id") + ")")
        elif line.get("attributes").get("description") == "Rapid Transit":
            metro.append(line.get("attributes").get("long_name") + " (ID: " + line.get("id") + ")")
        elif line.get("attributes").get("description") == "Key Bus":
            bus.append(line.get("attributes").get("long_name") + " (ID: " + line.get("id") + ")")
    print(linesJson['data'])
    commuter_rail = "\n".join(commuter_rail)
    metro = "\n".join(metro)
    bus = "\n".join(bus)
    return [commuter_rail,metro,bus]

def schedule():
# will be implemented later, am just putting in the time to be used for future commands
    wday = time.localtime().tm_wday
    month = time.localtime().tm_mon
    day = time.localtime().tm_mday
    hr = time.localtime().tm_hour
    min = time.localtime().tm_min
    dst = time.localtime().tm_isdst
    return "it's " + str(wday) + ", " + str(month) + " " + str(day) + ", " + str(hr) + ":" + str(min) + " and dst is " + str(dst)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(schedule())
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
    if len("\n".join(a)) > 1024:
        a = "Stops unavailable (Character limit exceeded!)"
    else:
        a = "\n".join(a)
    zipped = list(zip(termini, direction))
    test = zipped[0][0] + " ("+zipped[0][1]+ ")\n" + zipped[1][0] + " ("+zipped[1][1]+")"
    embedVar = discord.Embed(title= line, description="Information for **" + line + "** Line", color=color)
    embedVar.add_field(name="Termini", value= test, inline=False)
    embedVar.add_field(name="Stops", value= a, inline=False)
    try:
        await ctx.send(embed=embedVar)
    except:
        await ctx.send("An error occurred. Please try again!")

@bot.command()
async def getlines(ctx):
    big_list = (getLinesFunc())
    embedVar = discord.Embed(title="MBTA Lines", description="All MBTA transportation lines", color=6750873)
    embedVar.add_field(name="Commuter Rail", value=big_list[0], inline=False)
    embedVar.add_field(name="Metro", value=big_list[1], inline=False)
    embedVar.add_field(name="Bus", value=big_list[2], inline=False)
    await ctx.send(embed=embedVar)

@bot.command()
async def help(ctx):
    embedVar = discord.Embed(title="Help", description="List of all commands", color=6750873)
    embedVar.add_field(name="info + [line name]",
                       value="Command to get info about a specific line (Commuter Rail + Metro)", inline=False)
    embedVar.add_field(name="getlines", value="Get a list of all Commuter Rail, Metro, and Buses", inline=False)
    embedVar.add_field(name="getmap", value="Get a map of the mbta", inline=False)
    embedVar.add_field(name="getmapCR", value="Get a map of the mbta including commuter rail", inline=False)
    embedVar.add_field(name="metro", value="Get a list of the names of the metro lines", inline=False)
    embedVar.add_field(name="CR", value="Get a list of the names of the Commuter Rail ", inline=False)
    await ctx.send(embed=embedVar)
    
@bot.command()
async def metro(ctx):
    embedVar = discord.Embed(title="Metro", description="Red \n Orange \n Blue \n green", color=16777215)
    await ctx.send(embed=embedVar)

@bot.command()
async def CR(ctx):
    embedVar = discord.Embed(title="Commuter Rail", description="Fairmount \n Fitchburg \n Worcester \n Franklin \n Greenbush \n Haverhill \n Kingston \n Middleborough \n Needham \n Newburyport \n Providence \n Foxboro",color=16777215)
    await ctx.send(embed=embedVar)

@bot.command()
async def getmap(ctx):
    await ctx.send(file=discord.File('MBTA MAP.jpg'))

@bot.command()
async def getmapCR(ctx):
    await ctx.send(file=discord.File('CR MAP.png'))
   
bot.run('')
