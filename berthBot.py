import discord
from discord.ext import commands
from datetime import datetime
import os
import asyncio
import re

from berthObj import *
client = commands.Bot(command_prefix = '!')

async def daily_check():
    berthFlag = False
    greeting_time = '10:00'
    tempBDAY = ' '

    await client.wait_until_ready()
    print("I AM READY!")
    msg_channel = client.get_channel(123456)
    
    while not client.is_closed():
        # checkFile = open(r"path","r")
        checkFile = open(r"D:\Users\Roy Matthew\Documents\Side_Projs\berthBot\berthList1.txt","r")
        checkLine = checkFile.readline()

        while checkLine:
            tempCL = checkLine.split(" ")
            now = datetime.now()
       
            CL = tempCL[1]
            date_today = now.strftime('%m/%d')
            # print(f'tempCL[1]:{CL[:-1]} now:{date_today}')
            if(CL[:-1] == date_today):
                print('Found equal dates!')
                tempBDAY = tempCL[0]
                berthFlag = True
            
            checkLine = checkFile.readline()
           
        checkFile.close()

        time_now = datetime.strftime(datetime.now(),'%H:%M')
        # print(f'greeting time:{greeting_time} time_now:{time_now}')
        
        if(greeting_time == time_now and berthFlag == True):
            print("it is time!")
            await msg_channel.send(f'Happiest Birthday to {tempBDAY}!')
            print("birthday greeting sent!")
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
    await ctx.send("Berth is awake and is functional!")

# Command for adding a birthday 
# in order to execute, type: !b_add @user bday(MM/DD)
@client.command() 
async def b_add(ctx, member, date):

    tempID = re.split('<|!|>',member)
    some_id = int(tempID[2]) if tempID[2] != None else  int(tempID[3])
    user_id = client.get_user(some_id)

    bObj = Birthday(member, date, user_id)
    dateFlag = True
    buff = 0

    # buffer variable that splits the bdate in order to check the validity of the input
    tempDate = bObj.bday.split("/")
    month = int(tempDate[0])
    day = int(tempDate[1])

    # try and except blocks that test the validity of the birth date
    try:
        
        if month > 13 or month < 1:
            await ctx.send("There are only 12 months in a year")
            dateFlag = False
        else:
            # await ctx.send("Passing throuh reason 1.")
            pass

        if month in (1, 3, 5, 7, 8, 10, 12):
            if day > 31 or day < 1:
                await ctx.send(f'There are only 31 days in month {month}')
                dateFlag = False
            else:
                # await ctx.send("Passing throuh reason 2.")
                pass
        elif month in (4, 6, 9, 11):
            if day > 30 or day < 1:
                await ctx.send(f'There are only 30 days in month {month}')
                dateFlag = False
            else:
                # await ctx.send("Passing throuh reason 3.")
                pass
        elif month == 2:
            if day > 29 or day < 1:
                await ctx.send(f'There are only 29 possible days in month {month}')
                dateFlag = False
            else:
                # await ctx.send("Passing throuh reason 4.")
                pass
    except:
        await ctx.send("You just entered an invalid date.")
        dateFlag = False
    
    # addFile stores the opened file, path will vary 
    # BerthBot runs on a raspberry pi so path will follow a linux convention
    addFile = open('filepath',"r+")

    # reads each line and modifies the 'buff' variable if the user already has an inputted birthdate
    line = addFile.readline()
    while line and buff != 1:
        if bObj.user in line:
            print(f'{bObj.user_num} is in {line}')
            buff = 1
        elif bObj.user not in line:
            buff = 0
        line = addFile.readline()

    # validity checks and makes sure that the dates are valid and that here aren't any duplicate users with birthdays
    if (buff == 1):
        await ctx.send(f'{bObj.user_num} is already on the BerthList!')
    elif(buff == 0 and dateFlag == True):
        addFile.write(f"{bObj.user_id} {bObj.bday} {bObj.user_num}\n")
        await ctx.send(f'{bObj.user_num} whose birthday is on {bObj.bday} has been added to the Berth List!')

    # print(os.path.abspath('berthList1.txt'))
    # addFile = open(os.path.abspath('berthList1.txt'),"a")

    addFile.close()


# client.loop.create_task(daily_check())

client.run('TOKEN')

