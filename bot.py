import discord
from reaction import *
import ffmpeg
from discord.ext import commands
BOT_TOKEN = 'MTMyMjMxMDY4OTI3NjAzNTA5Mg.G4Ed-y.cZ5kiofk2hYgg-Ic8m_3xTPEA7Cj5AFwQO7SZw'
CHANNEL_ID =  507666860968247298

intents = discord.Intents.default()
intents.message_content = True

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.command()
async def join(ctx):
    """Command to join a voice channel"""
    # Check if the user is in a voice channel
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        # Connect to the channel
        await channel.connect()
        await ctx.send(f"Joined {channel.name}!")
    else:
        await ctx.send("You need to be in a voice channel for me to join!")

@bot.command()
async def leave(ctx):
    """Command to leave a voice channel"""
    # Check if the bot is in a voice channel
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel!")
    else:
        await ctx.send("I'm not in a voice channel!")

@bot.command()
async def react(ctx):
    """Command to play a sound in the voice channel"""
    if not ctx.voice_client:
        await ctx.send("I'm not connected to a voice channel! Use !join to connect me.")
        return

    try:
        # Ensure the bot is connected to a voice channel
        vc = ctx.voice_client

        # Prepare the audio source using FFmpeg
        sound_url = grab_reaction()
        direct_path = 'C:/ffmpeg/ffmpeg-2024-12-26-git-fe04b93afa-essentials_build/bin/ffmpeg'
        audio_source = discord.FFmpegPCMAudio(executable=direct_path , source= "Reactions/GrabBag/" + sound_url)
        if not vc.is_playing():
            vc.play(audio_source, after=lambda e: print(f"Error: {e}") if e else None)
            #await ctx.send(f"Now playing: {sound_url}")
        else:
            await ctx.send("Already playing audio. Please wait until it's finished.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.event
async def on_reaction_add(reaction, user):
    # Check for thumbs up reaction
    if "react" == reaction.emoji.name:
        reacted = react_text()
        await reaction.message.reply(reacted)


bot.run(BOT_TOKEN)