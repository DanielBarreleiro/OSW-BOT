import discord
from discord.ext import tasks, commands
import urllib
import urllib.parse
from datetime import datetime
import time
import calendar
import json
import requests
from secrets import *
# Google API
import gspread
from oauth2client.service_account import ServiceAccountCredentials

client = discord.Client()


@tasks.loop(seconds=0.0, minutes=0.0, hours=1.0)
async def slow_count():

    # USE API'S AND USE CREDS
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gc = gspread.authorize(creds)

# ALLIANCE VALUE CALLS
    # OPEN THIS FILE - ALLIANCE VALUE
    sheet = gc.open("AllianceValue")
    # GET CURRENT MONTH
    month_n = datetime.today().strftime('%m')
    month = calendar.month_name[int(month_n)]
    # GET WORKSHEET BASED ON MONTH - ALLIANCE VALUE
    worksheet = sheet.worksheet(month)
    # GET CURRENT DAY + 1 - ALLIANCE VALUE
    day = int(datetime.today().strftime('%d')) + 1
    print(day)
    # GET CURRENT HOUR - ALLIANCE VALUE
    now = datetime.now().strftime('%H')
    print("Hour:")
    print(now)
    # COLLUMNS - ALLIANCE VALUE
    midday_col = 2
    midnight_col = 3
# ALLIANCE VALUE CALLS END -------

    # GET DATA
    response = requests.post(url)
    response.raise_for_status()
    results = response.json()

    if now == '12':
        worksheet.update_cell(day, midday_col, str(results['alliance'][0]['value']))
        print("Alliance Value done")
        print("12 edit")
    elif now == '00':
        day2 = int(datetime.today().strftime('%d'))
        worksheet.update_cell(day2, midnight_col, str(results['alliance'][0]['value']))
        print("00 edit")
        print("Alliance Value done")
    print("loop restarting")
slow_count.start()

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

    if message.content.startswith('!alliance'):
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        embed = discord.Embed(title="Alliance Stats", color=0x00ffff)
        embed.add_field(name="Value", value='$' + str(results['alliance'][0]['value']), inline=True)
        embed.add_field(name="Rank", value=str(results['alliance'][0]['rank']), inline=True)
        embed.set_footer(text="By: TOYOTA - AIR")
        await message.channel.send(embed=embed)

    elif message.content.startswith('!stats' + airname):
        #Alliance
        airname = message.content
        airname = airname.replace('!stats ', '')
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        for member in results['members']:
            try:
                if member['company'] == airname:
                    #Airline
                    response = requests.post(user_url + '&user=' + airname)
                    response.raise_for_status()
                    results_a = response.json()
                    #----
                    today = int(time.time())
                    cont = member['contributed']
                    join = int(member['joined'])
                    # unix time things..
                    unix_diff = today - join
                    diff = round(unix_diff / 86400)
                    # ---
                    avg = cont / diff
                    airname = airname.replace('!stats ', '')
                    embed = discord.Embed(title=airname + "  |  Stats", color=0x00ffff)
                    embed.add_field(name="Flights", value=str(member['flights']), inline=True)
                    embed.add_field(name="Contribution", value='$' + str(cont / 1000), inline=True)
                    embed.add_field(name="Average Contribution p/day", value='$' + str(round(avg, 3)), inline=True)
                    embed.add_field(name="Mode", value=str(results_a['user']['game_mode']), inline=True)
                    embed.add_field(name="Rank", value=str(results_a['user']['rank']), inline=True)
                    embed.add_field(name="Share Value", value='$' + str(results_a['user']['share']), inline=True)
                    embed.add_field(name="Level", value=str(results_a['user']['level']), inline=True)
                    embed.add_field(name="Fleet", value=str(results_a['user']['fleet']), inline=True)
                    embed.add_field(name="Routes", value=str(results_a['user']['routes']), inline=True)
                    embed.set_thumbnail(url=results_a['user']['logo'])
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

    #ADMIN COMMANDS ------------------------------------
    elif message.content.startswith('!dailyc'):
        response = requests.post(url)
        response.raise_for_status()
        results = response.json()
        role = 701902159159099439
        if role in [y.id for y in message.author.roles]:
            n = 0
            dailyc = "ONE STAR WORLD | DAILY CONTRIBUTION \n\n"
            for member in results['members']:
                today = int(time.time())
                comp = str(results['members'][n]['company'])
                cont = int(results['members'][n]['contributed'])
                join = int(results['members'][n]['joined'])
                # unix time things..
                unix_diff = today - join
                diff = round(unix_diff / 86400)
                if diff == 0:
                    break
                # ---
                avg = cont / diff
                dailyc = dailyc + "Member: " + comp + "\n" + "Contribution p/day: $" + str(round(avg, 3)) + "\n\n"
                n = n + 1
            pb_v = {'api_dev_key':str(pbk), 'api_option':'paste', 'api_paste_expire_date':'1H', 'api_paste_name':'ONE STAR WORLD | Daily Constribution','api_paste_code':str(dailyc)}
            data = urllib.parse.urlencode(pb_v).encode("utf-8")
            req = urllib.request.Request('http://pastebin.com/api/api_post.php')
            with urllib.request.urlopen(req, data=data) as f:
                resp = f.read()
                resp = resp.decode('utf-8')
                await message.channel.send(resp)
        else:
            await message.channel.send(":x: You're not a Manager, you can't use this command.")

client.run(token)
