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

sheet = gc.open("AllianceValue")
#GET CURRENT MONTH
month_n = datetime.today().strftime('%m')
month = calendar.month_name[int(month_n)]
#GET WORKSHEET BASED ON MONTH
worksheet = sheet.worksheet(month)

#GET CURRENT DAY + 1
day = int(datetime.today().strftime('%d')) + 1
#GET ROW BY DAY
midday_col = 2
midnight_col = 3
#worksheet.update_cell(10, midday_row, 'test')
#------------------
#now = datetime.now().strftime('%H')
#-------
#loop(seconds=2, minutes=0, hours=0, count=None, reconnect=True)
#if now == '12':
#if message.content.startswith('!dayval'):
#    response = requests.post(url)
#    response.raise_for_status()
#    results = response.json()
#    worksheet.update_cell(day, midday_col, str(results['alliance'][0]['value']))
#if now == '21':
#    print('k')
#if now == '00':
#if message.content.startswith('!nightval'):
#    response = requests.post(url)
#    response.raise_for_status()
#    results = response.json()
#    worksheet.update_cell(day, midnight_col, str(results['alliance'][0]['value']))


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

    if message.content.startswith('!dayval'):
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        worksheet.update_cell(day, midday_col, str(results['alliance'][0]['value']))

    if message.content.startswith('!nightval'):
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        worksheet.update_cell(day, midnight_col, str(results['alliance'][0]['value']))

    if message.content.startswith('!alliance'):
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        embed = discord.Embed(title="Alliance Stats", color=0x00ffff)
        embed.add_field(name="Value", value='$' + str(results['alliance'][0]['value']), inline=True)
        embed.add_field(name="Rank", value=str(results['alliance'][0]['rank']), inline=True)
        embed.set_footer(text="By: TOYOTA - AIR")
        await message.channel.send(embed=embed)

    elif message.content.startswith('!pstats' + airname):
        airname = message.content
        airname = airname.replace('!pstats ', '')
        try:
            response = requests.post(user_url + '&user=' + airname)
            response.raise_for_status()
            results = response.json()
            embed = discord.Embed(title= airname + "  |  Stats", color=0x00ffff)
            embed.add_field(name="Level", value=str(results['user']['level']), inline=False)
            embed.add_field(name="Share Value", value='$' + str(results['user']['share']), inline=False)
            embed.add_field(name="Fleet", value=str(results['user']['fleet']), inline=False)
            embed.add_field(name="Routes", value=str(results['user']['routes']), inline=False)
            embed.set_footer(text="By: TOYOTA - AIR")
            await message.channel.send(embed=embed)
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
                    airname = airname.replace('!stats ', '')
                    embed = discord.Embed(title=airname + "  |  Alliance Stats", color=0x00ffff)
                    embed.add_field(name="Flights", value=str(member['flights']), inline=False)
                    embed.add_field(name="Contribution", value='$' + str(cont), inline=False)
                    embed.add_field(name="Share Value", value='$' + str(member['shareValue']), inline=False)
                    embed.set_footer(text="By: TOYOTA - AIR")
                    await message.channel.send(embed=embed)
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
     #   channel = client.get_channel(703342736568352809)
        #await channel.send("Don't worry, the bot hasn't freaked out! Its just being updated!")
        #+ "\n" + 'Tag <@&703342736568352809>  !')
      #  await channel.send(embed=embed)

client.run(token)