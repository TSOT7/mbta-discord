import discord
from discord.ext import commands
import requests
import time
import json

description = "Basic bot used to connect to MBTA."
bot = commands.Bot(command_prefix='mbta!', description=description)

weekday = {'0': 'Monday', '1': 'Tuesday', '2': 'Wednesday', '3': 'Thursday', '4': 'Friday', '5': 'Saturday',
           '6': 'Sunday'}
hr = time.localtime().tm_hour
min = time.localtime().tm_min
wday = time.localtime().tm_wday
month = time.localtime().tm_mon
day = time.localtime().tm_mday
year = time.localtime().tm_year


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
    return [commuter_rail, metro, bus]


def stopToID(line, stop):
    stops = requests.get("https://api-v3.mbta.com/stops?filter[route]=" + line.title()).json()
    for a in stops['data']:
        if a.get("attributes").get("name") == stop:
            b = a.get("id")
            return b


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print("Local Time: " + str(hr) + ":" + str(min) + ", " + weekday[str(wday)] + ", " + str(month) + "/" + str(
        day) + "/" + str(year))
    print('------')


@bot.command()
async def info(ctx, line):
    if line.title() in (
    'Fairmount', 'Fitchburg', 'Worcester', 'Franklin', 'Greenbush', 'Haverhill', 'Kingston', 'Lowell', 'Middleborough',
    'Needham', 'Newburyport', 'Providence'):
        line = "CR-" + line.title()
        print(line)
    if "CR-" not in line.upper():
        line = line.title()
    elif "green" in line.lower():
        line = "Green-" + line[-1]
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
    test = zipped[0][0] + " (" + zipped[0][1] + ")\n" + zipped[1][0] + " (" + zipped[1][1] + ")"

    if "CR-" in line:
        aterm = " or ".join(termini).split(" or ")
    else:
        aterm = "/".join(termini).split("/")
    b = ""
    print(aterm)
    for term in aterm:
        if "CR-" in line:
            print(stopToID(line,term))
            # if "Station" in term:
            #     predictions = requests.get("https://api-v3.mbta.com//schedules?filter[stop]=" + stopToID(line,term) + "&page[limit]=1&filter[direction_id]=0").json()
            # else:
            #     predictions = requests.get("https://api-v3.mbta.com//schedules?filter[stop]=" + stopToID(line,term) + "&page[limit]=1&filter[direction_id]=1").json()
            b = "Not supported at the moment :("
        else:
            predictions = requests.get("https://api-v3.mbta.com//predictions?filter[stop]=" + stopToID(line,term) + "&page[limit]=1").json()
            for predict in predictions['data']:
                b += term + ": " + (predict.get('attributes').get('departure_time')[:19].replace("T",", ")) + "\n"

    embedVar = discord.Embed(title=line, description="Information for **" + line + "** Line", color=color)
    embedVar.add_field(name="Termini", value=test, inline=False)
    embedVar.add_field(name="Stops", value=a, inline=False)
    embedVar.add_field(name="Next Departures", value=b, inline=False)
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
async def commands(ctx):
    embedVar = discord.Embed(title="Commands", description="List of all commands", color=6750873)
    embedVar.add_field(name="info + [line name]",
                       value="Command to get info about a specific line (Commuter Rail + Metro)", inline=False)
    embedVar.add_field(name="getlines", value="Get a list of all Commuter Rail, Metro, and Buses", inline=False)
    embedVar.add_field(name="commands", value="Get a list of all commands", inline=False)
    await ctx.send(embed=embedVar)


@bot.command()
async def time(ctx):
    await ctx.send(
        "Local Time: " + str(hr) + ":" + str(min) + ", " + weekday[str(wday)] + ", " + str(month) + "/" + str(
            day) + "/" + str(year))

bot.run('')
