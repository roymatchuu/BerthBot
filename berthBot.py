import discord
from discord.ext import commands
from datetime import datetime
import os
import asyncio

from berthObj import *
client = commands.Bot(command_prefix = '!')

async def daily_check():
    berthFlag = False
    greeting_time = '10:00'
    tempBDAY = ' '

    await client.wait_until_ready()
    print("I AM READY!")
    msg_channel = client.get_channel(123456)
    
    # msgs = cycle(status)

    while not client.is_closed():
        print("SELF IS NOT CLOSED!!!")

        checkFile = open(r"path","r")
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
        print(f'greeting time:{greeting_time} time_now:{time_now}')
        
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

# Command for adding a birthday 
# in order to execute, type: !b_add @user bday(MM/DD)
@client.command() 
async def b_add(ctx, member, date):
    bObj = Birthday(member, date)
    dateFlag = True
    buff = 0

    # buffer variable that splits the bdate in order to check the validity of the input
    tempDate = bObj.bday.split("/")

    # try and except blocks that test the validity of the birth date
    try:
        if tempDate[0] > 13 or tempDate[0] < 1:
            await ctx.send("Invalid date.")
            dateFlag = False
        else:
            pass

        if tempDate[0] in (1, 3, 5, 7, 8, 10, 12):
            if tempDate[1] > 31 or tempDate[1] < 1:
                await ctx.send("Invalid date.")
                dateFlag = False
            else:
                pass
        elif tempDate[0] in (4, 6, 9, 11):
            if tempDate[1] > 30 or tempDate[1] < 1:
                await ctx.send("Invalid date.")
                dateFlag = False
            else:
                pass
        elif tempDate[0] == 2:
            if tempDate[1] > 29 or tempDate[1] < 1:
                await ctx.send("Invalid date.")
                dateFlag = False
            else:
                pass
    except:
        await ctx.send("Invalid date.")
        dateFlag = False
    
    # addFile stores the opened file, path will vary 
    # BerthBot runs on a raspberry pi so path will follow a linux convention
    addFile = open('filepath',"r+")

    # reads each line and modifies the 'buff' variable if the user already has an inputted birthdate
    line = addFile.readline()
    while line and buff != 1:
        if bObj.user in line:
            print(f'{bObj.user} is in {line}')
            buff = 1
        elif bObj.user not in line:
            buff = 0
        line = addFile.readline()

    # validity checks and makes sure that the dates are valid and that here aren't any duplicate users with birthdays
    if (buff == 1):
        await ctx.send(f'{bObj.user} is already on the BerthList!')
    elif(buff == 0 and dateFlag == True):
        addFile.write(f"{bObj.user} {bObj.bday}\n")
        await ctx.send(f'{bObj.user} whose birthday is on {bObj.bday} has been added to the Berth List!')

    # print(os.path.abspath('berthList1.txt'))
    # addFile = open(os.path.abspath('berthList1.txt'),"a")

    addFile.close()




client.loop.create_task(daily_check())
client.run('TOKEN')

