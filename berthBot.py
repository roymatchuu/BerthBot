import discord
from discord.ext import commands
from datetime import datetime
import os
import asyncio
import re
import traceback

from berthObj import *
# delimeter = '!'
client = commands.Bot(command_prefix = '!')

async def daily_check():
    berthFlag = False
    greeting_time = '13:24'
    tempBDAY = ' '

    await client.wait_until_ready()
    # print("I AM READY!")
    msg_channel = client.get_channel(123456)
    bday_bucket = set()
    
    while not client.is_closed():
        # checkFile = open(r"path","r")
        checkFile = open(r"berthList1.txt","r")
        checkLine = checkFile.readline()

        if(checkLine != None):
            while checkLine:
                tempCL = checkLine.split(" ")
                now = datetime.now()
        
                CL = tempCL[1]
                date_today = now.strftime('%m/%d')
                # print(f'tempCL[1]:{CL} now:{date_today}')
                if(CL == date_today):
                    # print('Found equal dates!')
                    tempBDAY = tempCL[2]
                    berthFlag = True
                    bday_bucket.add(tempBDAY)
                
                checkLine = checkFile.readline()
        

        checkFile.close()

        time_now = datetime.strftime(datetime.now(),'%H:%M')
        # print(f'greeting time:{greeting_time} time_now:{time_now}')
        
        if(greeting_time == time_now and berthFlag == True):
            # print("it is time!")
            for bdays in bday_bucket:
                await msg_channel.send(f'Happiest Birthday to {bdays}')
                print("birthday greeting sent!")
            bday_bucket.clear()

            time = 60
        else: 
            time = 1
        await asyncio.sleep(time)

# Sets Berth's status to online and the status message 
@client.event 
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(name="Berthday Song"))
    print("berthy is online!")

# ping command to see if berth is functional
@client.command()
async def ping(ctx):
    await ctx.send("```Berth is awake and is functional!```")

# Command for adding a birthday 
# in order to execute, type: !add @user bday(MM/DD)
@client.command() 
async def add(ctx, member, date):

    try:
        tempID = re.split('<|!|>',member)
        some_id = int(tempID[2]) if tempID[2] != None else  int(tempID[3])
        user_id = client.get_user(some_id)

        bObj = Birthday(member, date, user_id)
        dateFlag = True
        buff = 99

        # buffer variable that splits the bdate in order to check the validity of the input
        tempDate = bObj.bday.split("/")
        month = int(tempDate[0])
        day = int(tempDate[1])

            # try and except blocks that test the validity of the birth date
        try:
            
            if month > 13 or month < 1:
                await ctx.send("```There are only 12 months in a year```")
                dateFlag = False
            else:
                pass

            if month in (1, 3, 5, 7, 8, 10, 12):
                if day > 31 or day < 1:
                    await ctx.send(f'```There are only 31 days in month {month}```')
                    dateFlag = False
                else:
                    pass
            elif month in (4, 6, 9, 11):
                if day > 30 or day < 1:
                    await ctx.send(f'```There are only 30 days in month {month}```')
                    dateFlag = False
                else:
                    pass
            elif month == 2:
                if day > 29 or day < 1:
                    await ctx.send(f'```There are only 29 possible days in month {month}```')
                    dateFlag = False
                else:
                    pass
        except:
            await ctx.send("```You just entered an invalid date.```")
            dateFlag = False

        # addFile stores the opened file, path will vary 
        # BerthBot runs on a raspberry pi so path will follow a linux convention
        # addFile = open('filepath',"r+")
        addFile = open(r"berthList1.txt", "r+")

        # reads each line and modifies the 'buff' variable if the user already has an inputted birthdate
        line = addFile.readline()
        while line or buff != 1:
            if not line:
                buff = 0
                break
            elif bObj.user_num in line:
                print(f'{bObj.user_id} is in {line}')
                buff = 1
                break
            else:
                line = addFile.readline()

        if(month < 10):
            bObj.bday = '0' + bObj.bday
        
        # validity checks and makes sure that the dates are valid and that here aren't any duplicate users with birthdays
        if (buff == 1):
            await ctx.send(f'{bObj.user_id} is already on the BerthList!')
        elif(buff == 0 and dateFlag == True):
            addFile.write(f"{bObj.user_id} {bObj.bday} {bObj.user_num}\n")
            await ctx.send(f"`{bObj.user_id}'s birthday added!`")
        
        addFile.close()

    except Exception:
        await ctx.send("```Invalid input, please try adding again.```")

        # for debugging purposes only
        traceback.print_exc()

    

client.loop.create_task(daily_check())

client.run('TOKEN')

