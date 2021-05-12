import discord
from discord.ext import commands

from dhooks import Webhook
import requests


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '!', intents=intents)


@client.event
async def on_ready():
    print("We have logged in as {0.user}"
    .format(client))





    

@client.event
async def on_member_join(member):
    guild = client.get_guild(837400158839898122)
    channel = guild.get_channel(837400270324760597)
    await channel.send(f'Welcome to the server {member.mention}!')
    await member.send(f'Welcome to the {guild.name}, {member.name}!')



@client.command(pass_context = True)
async def join(ctx):
    
    if(ctx.author.voice):
        
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel! You must be in a voice channel to run this command.")
    


@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("I left the voice channel")
    else:
        await ctx.send("I am not in a voice channel.")
    


with open('token.txt', 'r', encoding='utf-8') as f:
    token = f.read()


client.run(token)