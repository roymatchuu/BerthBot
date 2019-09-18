import discord
from discord.ext import commands
import datetime
import os

from berthObj import *

client = commands.Bot(command_prefix = '!')

@client.event 
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game(name="Berthday Song"))
    print("berthy is online!")

@client.command() 
async def b_add(ctx, member, date):
    bObj = Birthday(member, date)

    dateFlag = True
    tempDate = bObj.bday.split("/")

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
    

     
    addFile = open('filepath',"r+")
    buff = 0

    line = addFile.readline()
    while line and buff != 1:
        if bObj.user in line:
            print(f'{bObj.user} is in {line}')
            buff = 1
        elif bObj.user not in line:
            buff = 0
        line = addFile.readline()


    # print(f'buff: {buff} and dateFlag: {dateFlag}')
    if (buff == 1):
        await ctx.send(f'{bObj.user} is already on the BerthList!')
    elif(buff == 0 and dateFlag == True):
        addFile.write(f"{bObj.user} {bObj.bday}\n")
        await ctx.send(f'{bObj.user} whose birthday is on {bObj.bday} has been added to the Berth List!')





    # print(os.path.abspath('berthList1.txt'))
    # addFile = open(os.path.abspath('berthList1.txt'),"a")

     
    
    addFile.close()

    
client.run('TOKEN')

