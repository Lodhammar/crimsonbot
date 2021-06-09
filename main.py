import discord
from discord import FFmpegPCMAudio
from dhooks import Webhook
import requests
from discord.ext import commands
import json
import os


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '!', intents=intents)
os.chdir(r'C:\Users\seanl\Documents\pythonbot')



@client.event
async def on_ready():
    print("We have logged in as {0.user}"
    .format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Shrek"))


@client.event
async def on_member_join(member):
    guild = client.get_guild(837400158839898122)
    channel = guild.get_channel(837400270324760597)
    await channel.send(f'Welcome to the server {member.mention}!')
    await member.send(f'Welcome to the {guild.name}, {member.name}!')

    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)



@client.event 
async def on_message(message):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json', 'w') as f:
        json.dump(users, f)

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
        await client.send(channel, '{} has leveled up to level {}'.format(user.mention), lvl_end)

@client.command(pass_context = True)
async def join(ctx):
    
    if(ctx.author.voice):
        
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('heavenfalls.mp3')
        player = voice.play(source)
    else:
        await ctx.send("You are not in a voice channel! You must be in a voice channel to run this command.")
    


@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel.")

@client.command(pass_context=True)
async def nick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention}')


@client.command(pass_context=True)
async def info(ctx):
    await ctx.send("You can communicate with people on the server and talk with them in voicechat.")



with open('token.txt', 'r', encoding='utf-8') as f:
    token = f.read()


client.run(token)