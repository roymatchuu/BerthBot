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


    if (buff == 1):
        await ctx.send(f'{bObj.user} is already on the BerthList!')
    elif(buff == 0):
        addFile.write(f"{bObj.user} {bObj.bday}\n")
        await ctx.send(f'{bObj.user} whose birthday is on {bObj.bday} has been added to the Berth List!')





    # print(os.path.abspath('berthList1.txt'))
    # addFile = open(os.path.abspath('berthList1.txt'),"a")

     
    
    addFile.close()

    
client.run('TOKEN')
