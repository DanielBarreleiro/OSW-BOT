import discord
from datetime import datetime
import json
import requests
from secrets import *

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity = discord.Activity(type=discord.ActivityType.watching, name="the Alliance"))

@client.event
async def on_message(message):
    airname = ''
    if message.author == client.user:
        return

    if message.content.startswith('!value'):
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        now = datetime.now()
        now = now.strftime("%H:%M")
        await message.channel.send('Alliance Value at ' + str(now) + ': $' + str(results['alliance'][0]['value']))

    #TOO DANGEROUS TO BE USED
    #elif message.content.startswith('!all'):
    #    response = requests.post(url)
    #    response.raise_for_status()
    #    results = response.json()
    #    now = datetime.now()
    #    now = now.strftime("%H:%M")
    #    n = 0
    #    for member in results['members']:
    #        await message.channel.send('Alliance Members Stats at ' + str(now))
    #        await message.channel.send('Member: ' + str(results['members'][n]['company']))
    #        await message.channel.send('Flights: ' + str(results['members'][n]['flights']))
    #        await message.channel.send('Contributed: ' + str(results['members'][n]['contributed']))
    #        await message.channel.send('IPO Value: ' + str(results['members'][n]['shareValue']))
    #        await message.channel.send('-----------------------------')
    #        n = n + 1

    elif message.content.startswith('!pstats' + airname):
        airname = message.content
        airname = airname.replace('!pstats ', '')
        response = requests.post(user_url + '&user=' + airname)
        response.raise_for_status()
        results = response.json()
        print(user_url + '&user=' + airname)
        await message.channel.send('Showing results for Airline: ' + airname)
        await message.channel.send('Level: ' + str(results['user']['level']))
        await message.channel.send('Share Value: $' + str(results['user']['share']))
        await message.channel.send('Fleet: ' + str(results['user']['fleet']))
        await message.channel.send('Routes: ' + str(results['user']['routes']))

    elif message.content.startswith('!stats' + airname):
        airname = message.content
        airname = airname.replace('!stats ', '')
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        for member in results['members']:
            if member['company'] == airname:
                await message.channel.send('Showing results for Airline: ' + str(airname))
                await message.channel.send('Flights: ' + str(member['flights']))
                cont = member['contributed'] / 1000
                await message.channel.send('Contribution: $' + str(cont))
                await message.channel.send('Share Value: $' + str(member['shareValue']))

client.run(token)