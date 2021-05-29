import discord
from dhooks import Webhook
import requests
from discord.ext import commands
from discord import FFmpegPCMAudio
import youtube_dl
import os


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '!', intents=intents)



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




@client.command(pass_context = True)
async def join(ctx):
    
    if(ctx.author.voice):
        
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
     
    else:
        await ctx.send("You are not in a voice channel! You must be in a voice channel to run this command.")
    
@client.command(pass_context = True)
async def play(ctx, url:str):
    
    if(ctx.author.voice):
        
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()

        ydl_opts = {
            'format':'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'prefferedcodec':'mp3',
                'preferredquality':'192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, "song.mp3")
        
        source = FFmpegPCMAudio('song.mp3')
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
    await ctx.send("This server is cringe")




with open('token.txt', 'r', encoding='utf-8') as f:
    token = f.read()


client.run(token)