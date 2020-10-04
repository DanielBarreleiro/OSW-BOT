import discord
from discord.ext import tasks, commands
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import numpy as np
from datetime import datetime
import urllib
import urllib.parse
import base64
import time
import calendar
import json
import requests
import re
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
    response = requests.get(url)
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

    if message.content.startswith('$a'):
        alliance = message.content
        alliance = alliance.replace('$a ', '')

        response = requests.get(url + '&search=' + alliance)
        response.raise_for_status()
        results = response.json()

        rank = str(results['alliance'][0]['rank'])
        value = str(results['alliance'][0]['value'])
        members = str(results['alliance'][0]['members'])
        maxMembers = str(results['alliance'][0]['maxMembers'])

        embed = discord.Embed(title=f"{alliance}  |  Stats", color=0x00ffff)
        embed.add_field(name="Rank", value=f"{rank}", inline=True)
        embed.add_field(name="Value", value=f"${value}", inline=True)
        embed.add_field(name="Members", value=f"{members}/{maxMembers}", inline=False)
        embed.set_footer(text="By: TOYOTA - AIR")
        await message.channel.send(embed=embed)

    elif message.content.startswith('$s'):
        airname = message.content
        airname = airname.replace('$s ', '')
        print("User: " + airname)
        today = int(time.time())

        #GET airline data
        response = requests.get(url + '&user=' + airname)
        response.raise_for_status()
        airline = response.json()

        #SET airline data vars
        level = str(airline['user']['level'])
        share = str(airline['user']['share'])
        share_a = airline['user']['shares_available']
        share_s = airline['user']['shares_sold']
        share_t = share_a + share_s
        fleet = str(airline['user']['fleet'])
        routes = str(airline['user']['routes'])
        alliance = str(airline['user']['alliance'])
        gamemode = str(airline['user']['game_mode'])
        rank = str(airline['user']['rank'])

        # Write it down
        if alliance == 'False':
            embed = discord.Embed(title=airname + "  |  Stats", color=0x00ffff)
            embed.add_field(name="Rank", value=rank, inline=True)
            embed.add_field(name="Mode", value=gamemode, inline=True)
            embed.add_field(name="Fleet / Routes", value=fleet + '/' + routes, inline=True)
            embed.add_field(name="Level", value=level, inline=True)
            if share != '0':
                embed.add_field(name="Share Value", value=share, inline=True)
                embed.add_field(name="Share Market", value="Sold " + str(share_s) + '/' + str(share_t), inline=True)
                print('0', airline['share_development'][0]['date'])
                # Graph
                d0 = airline['share_development'][0]['date']
                d0 = datetime.fromtimestamp(int(d0)).strftime('%d %b, %H:%M')
                d2 = airline['share_development'][2]['date']
                d2 = datetime.fromtimestamp(int(d2)).strftime('%d %b, %H:%M')
                d4 = airline['share_development'][4]['date']
                d4 = datetime.fromtimestamp(int(d4)).strftime('%d %b, %H:%M')
                d6 = airline['share_development'][6]['date']
                d6 = datetime.fromtimestamp(int(d6)).strftime('%d %b, %H:%M')
                d8 = airline['share_development'][8]['date']
                d8 = datetime.fromtimestamp(int(d8)).strftime('%d %b, %H:%M')
                d10 = airline['share_development'][10]['date']
                d10 = datetime.fromtimestamp(int(d10)).strftime('%d %b, %H:%M')
                d12 = airline['share_development'][12]['date']
                d12 = datetime.fromtimestamp(int(d12)).strftime('%d %b, %H:%M')
                d14 = airline['share_development'][14]['date']
                d14 = datetime.fromtimestamp(int(d14)).strftime('%d %b, %H:%M')
                d16 = airline['share_development'][16]['date']
                d16 = datetime.fromtimestamp(int(d16)).strftime('%d %b, %H:%M')
                d19 = airline['share_development'][19]['date']
                d19 = datetime.fromtimestamp(int(d19)).strftime('%d %b, %H:%M')
                s0 = airline['share_development'][0]['share']
                s2 = airline['share_development'][2]['share']
                s4 = airline['share_development'][4]['share']
                s6 = airline['share_development'][6]['share']
                s8 = airline['share_development'][8]['share']
                s10 = airline['share_development'][10]['share']
                s12 = airline['share_development'][12]['share']
                s14 = airline['share_development'][14]['share']
                s16 = airline['share_development'][16]['share']
                s19 = airline['share_development'][19]['share']
                x = np.array([d19, d16, d14, d12, d10, d8, d6, d4, d2, d0])
                y = np.array([s19, s16, s14, s12, s10, s8, s6, s4, s2, s0])
                print(x)
                print(y)
                plt.figure(figsize=(15,5))
                plt.plot(x, y[:len(x)], marker=".")
                plt.xlabel('GMT')
                plt.title('SV History | ' + airname)
                plt.savefig(str(today) + '.png')
                with open(str(today) + '.png', "rb") as file:
                    bburl = "https://api.imgbb.com/1/upload"
                    payload = {
                        "key": ibb,
                        "image": base64.b64encode(file.read()),
                        "name": str(today),
                    }
                    res = requests.post(bburl, payload)
                    data = json.loads(res.text)['data'];
                    embed.set_image(url=data['url'])
                print('done')
            #embed.add_field(name="Founded", value=founded, inline=True)
                try:
                    path = re.search("(?P<url>https?://[^\s]+)", airline['user']['logo']).group("url")
                    embed.set_thumbnail(url=path)
                except:
                    embed.set_thumbnail(url='https://www.airline4.net/assets/img/logos/am_logo.png')
                embed.set_footer(text="By: TOYOTA - AIR")
                await message.channel.send(embed=embed)
            else:
                try:
                    path = re.search("(?P<url>https?://[^\s]+)", airline['user']['logo']).group("url")
                    embed.set_thumbnail(url=path)
                except:
                    embed.set_thumbnail(url='https://www.airline4.net/assets/img/logos/am_logo.png')
                embed.set_footer(text="By: TOYOTA - AIR")
                await message.channel.send(embed=embed)
        else:
            #GET alliance data
            response = requests.get(url + '&search=' + alliance)
            response.raise_for_status()
            alliance_data = response.json()

            #SET airline data vars
            #- Alliance
            a_name = str(alliance_data['alliance'][0]['name'])
            a_rank = str(alliance_data['alliance'][0]['rank'])
            a_members = str(alliance_data['alliance'][0]['members'])
            a_value = str(alliance_data['alliance'][0]['value'])
            #- Members
            for user in alliance_data['members']:
                if user['company'] == airname or airname in user['company']:
                    #----
                    today = int(time.time())
                    cont = user['contributed']
                    join = int(user['joined'])
                    ##----
                    unix_diff = today - join
                    diff = round(unix_diff / 86400)
                    ##----
                    avg = cont / diff

                    # SET alliance data vars
                    a_flights = str(user['flights'])
                    a_cont = cont
                    a_avgcont = str(round(avg))
                    #a_2dayavg = str(user['dailyContribution'])

            #-------------------------------------
            embed = discord.Embed(title=airname + "  |  Stats", color=0x00ffff)
            embed.add_field(name="\u200B", value=f"```Alliance: {a_name} \nRank: {a_rank} \nMembers: {a_members} \nValue: {a_value} \n -------- \nFlights: {a_flights} \nContribution: {a_cont:,d} \nAverage Contribution p/day: {a_avgcont} ```", inline=False)

            #embed.add_field(name="\u200B", value="\u200B", inline=False)
            #embed.add_field(name="\u200B", value="\u200B", inline=False)
            embed.add_field(name="Rank", value=rank, inline=True)
            embed.add_field(name="Mode", value=gamemode, inline=True)
            embed.add_field(name="Fleet / Routes", value=fleet + '/' + routes, inline=True)
            embed.add_field(name="Level", value=level, inline=True)
            print(share)
            if share != '0':
                embed.add_field(name="Share Value", value=share, inline=True)
                embed.add_field(name="Share Market", value="Sold " + str(share_s) + '/' + str(share_t), inline=True)
                # Graph
                d0 = airline['share_development'][0]['date']
                d0 = datetime.fromtimestamp(int(d0)).strftime('%d %b, %H:%M')
                d2 = airline['share_development'][2]['date']
                d2 = datetime.fromtimestamp(int(d2)).strftime('%d %b, %H:%M')
                d4 = airline['share_development'][4]['date']
                d4 = datetime.fromtimestamp(int(d4)).strftime('%d %b, %H:%M')
                d6 = airline['share_development'][6]['date']
                d6 = datetime.fromtimestamp(int(d6)).strftime('%d %b, %H:%M')
                d8 = airline['share_development'][8]['date']
                d8 = datetime.fromtimestamp(int(d8)).strftime('%d %b, %H:%M')
                d10 = airline['share_development'][10]['date']
                d10 = datetime.fromtimestamp(int(d10)).strftime('%d %b, %H:%M')
                d12 = airline['share_development'][12]['date']
                d12 = datetime.fromtimestamp(int(d12)).strftime('%d %b, %H:%M')
                d14 = airline['share_development'][14]['date']
                d14 = datetime.fromtimestamp(int(d14)).strftime('%d %b, %H:%M')
                d16 = airline['share_development'][16]['date']
                d16 = datetime.fromtimestamp(int(d16)).strftime('%d %b, %H:%M')
                d19 = airline['share_development'][19]['date']
                d19 = datetime.fromtimestamp(int(d19)).strftime('%d %b, %H:%M')
                s0 = airline['share_development'][0]['share']
                s2 = airline['share_development'][2]['share']
                s4 = airline['share_development'][4]['share']
                s6 = airline['share_development'][6]['share']
                s8 = airline['share_development'][8]['share']
                s10 = airline['share_development'][10]['share']
                s12 = airline['share_development'][12]['share']
                s14 = airline['share_development'][14]['share']
                s16 = airline['share_development'][16]['share']
                s19 = airline['share_development'][19]['share']
                x = np.array([d19, d16, d14, d12, d10, d8, d6, d4, d2, d0])
                y = np.array([s19, s16, s14, s12, s10, s8, s6, s4, s2, s0])
                print(x)
                print(y)
                plt.figure(figsize=(15,5))
                plt.plot(x, y[:len(x)], marker=".")
                plt.xlabel('GMT')
                plt.title('SV History | ' + airname)
                plt.savefig(str(today) + '.png')
                with open(str(today) + '.png', "rb") as file:
                    bburl = "https://api.imgbb.com/1/upload"
                    payload = {
                        "key": ibb,
                        "image": base64.b64encode(file.read()),
                        "name": str(today),
                    }
                    res = requests.post(bburl, payload)
                    data = json.loads(res.text)['data'];
                    embed.set_image(url=data['url'])
                print('done')
            #embed.add_field(name="Founded", value=founded, inline=True)
            else:
                try:
                    path = re.search("(?P<url>https?://[^\s]+)", airline['user']['logo']).group("url")
                    embed.set_thumbnail(url=path)
                except:
                    embed.set_thumbnail(url='https://www.airline4.net/assets/img/logos/am_logo.png')
            try:
                path = re.search("(?P<url>https?://[^\s]+)", airline['user']['logo']).group("url")
                embed.set_thumbnail(url=path)
            except:
                embed.set_thumbnail(url='https://www.airline4.net/assets/img/logos/am_logo.png')
            embed.set_footer(text="By: TOYOTA - AIR")
            await message.channel.send(embed=embed)

    elif message.content.startswith('$f' + price):
        price = message.content
        price = price.replace('$f ', '')
        channel = client.get_channel(706963574903275642)
        await channel.send('Fuel <@&706951098132594708> at $' + str(price) + ' !')
    elif message.content.startswith('$c' + price):
        price = message.content
        price = price.replace('$c ', '')
        channel = client.get_channel(706963574903275642)
        await channel.send('CO2 <@&706951098132594708> at $' + str(price) + ' !')

    #ADMIN COMMANDS ------------------------------------
    elif message.content.startswith('$dailyc'):
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
