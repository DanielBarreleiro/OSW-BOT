import discord
from datetime import datetime
import calendar
import json
import requests
from secrets import *
#Google API
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
gc = gspread.authorize(creds)
#----------

client = discord.Client()

#GET CURRENT MONTH
month_n = datetime.today().strftime('%m')
month = calendar.month_name[int(month_n)]
#GET SHEET AND WORKSHEET BASED ON MONTH
sheet = gc.open("AllianceValue")
worksheet = sheet.worksheet(month)
#worksheet.update_cell(10, 3, 'test')
#------------------
now = datetime.now().strftime('%H:%M')
#---
f = open("12row.txt","w+")
#---

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(status=discord.Status.online, activity = discord.Activity(type=discord.ActivityType.watching, name="the Alliance | By TOYOTA"))

@client.event
async def on_message(message):
    airname = ''
    price = ''
    if message.author == client.user:
        return

    #if now = '12:00':
    #    response = requests.post(url)
    #    response.raise_for_status()
    #    results = response.json()
    #    #worksheet.update_cell(7, 2, str(results['alliance'][0]['value']))
    #    f.write("%d" % (i + 1))

    #if now = '23:00':
    #    response = requests.post(url)
    #    response.raise_for_status()
    #    results = response.json()
        #worksheet.update_cell(7, 2, str(results['alliance'][0]['value']))
   #     f.write("%d" % (i + 1))

    if message.content.startswith('!alliance'):
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        await message.channel.send('Alliance Value: $' + str(results['alliance'][0]['value']) + "\n" +
        'Rank: ' + str(results['alliance'][0]['rank']))

    elif message.content.startswith('!pstats' + airname):
        airname = message.content
        airname = airname.replace('!pstats ', '')
        try:
            response = requests.post(user_url + '&user=' + airname)
            response.raise_for_status()
            results = response.json()
            await message.channel.send('Airline: ' + airname + "\n" +
            'Level: ' + str(results['user']['level']) + "\n" +
            'Share Value: $' + str(results['user']['share']) + "\n" +
            'Fleet: ' + str(results['user']['fleet']) + "\n" +
            'Routes: ' + str(results['user']['routes']))
        except:
            await message.channel.send("Airline not found!")

    elif message.content.startswith('!stats' + airname):
        airname = message.content
        airname = airname.replace('!stats ', '')
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        for member in results['members']:
            try:
                if member['company'] == airname:
                    cont = member['contributed'] / 1000
                    await message.channel.send('Airline: ' + str(airname) + "\n" +
                    'Flights: ' + str(member['flights']) + "\n" +
                    'Contribution: $' + str(cont) + "\n" +
                    'Share Value: $' + str(member['shareValue']))
            except:
                await message.channel.send("Airline not found!")

    elif message.content.startswith('!f' + price):
        price = message.content
        price = price.replace('!f ', '')
        channel = client.get_channel(706963574903275642)
        await channel.send('Fuel <@&706951098132594708> at $' + str(price) + ' !')
    elif message.content.startswith('!c' + price):
        price = message.content
        price = price.replace('!c ', '')
        channel = client.get_channel(706963574903275642)
        await channel.send('CO2 <@&706951098132594708> at $' + str(price) + ' !')

    #elif message.content.startswith('!osw'):
    #    channel = client.get_channel(706963574903275642)
    #    await channel.send("Don't worry, the bot hasn't freaked out! Its just being updated!" + "\n" +
    #    'Tag <@&706951098132594708>  !')

client.run(token)