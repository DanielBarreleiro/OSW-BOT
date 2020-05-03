import discord
from datetime import datetime
import json
import requests
from secrets import *

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!value'):
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        now = datetime.now()
        now = now.strftime("%H:%M")
        await message.channel.send('Alliance Value at ' + str(now) + ': $' + str(results['alliance'][0]['value']))

client.run(token)


#    for member in data['members']:
#        print('Member: ' + str(member['company']))
#        print('Flights: ' + str(member['flights']))
#        print('Contribution: ' + str(member['contributed']))
#        print('Share Value: ' + str(member['shareValue']))
#        print('-------------------')