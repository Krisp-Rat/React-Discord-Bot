import discord
import os
from reaction import *
from discord.ext import commands
import imageio_ffmpeg as ffmpeg

FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()

secret = 'MTMyMjMxMDY4OTI3NjAzNTA5Mg.G4Ed-y.cZ5kiofk2hYgg-Ic8m_3xTPEA7Cj5AFwQO7SZw'
BOT_TOKEN = os.environ.get('BOT_TOKEN', secret)

intents = discord.Intents.default()
intents.message_content = True

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
    else:
        await ctx.send("You need to be in a voice channel for me to join!")
    await ctx.message.delete()

@bot.command()
async def leave(ctx):
    """Command to leave a voice channel"""
    # Check if the bot is in a voice channel
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel!")
    await ctx.message.delete()

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
        #discord.AudioSource
        audio_source = discord.FFmpegPCMAudio(executable= FFMPEG_PATH , source= "Reactions/GrabBag/" + sound_url)
        if not vc.is_playing():
            vc.play(audio_source, after=lambda e: print(f"Error: {e}") if e else None)
            #await ctx.send(f"Now playing: {sound_url}")
        else:
            await ctx.send("Already playing audio. Please wait until it's finished.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

    await ctx.message.delete()

reacted_messages = []
@bot.event
async def on_reaction_add(reaction, user):
    # Check for thumbs up reaction
    print(reaction.message.id)
    if "react" == reaction.emoji.name and reaction.message.id not in reacted_messages:
        reacted = react_text()
        reacted_messages.append(reaction.message.id)
        await reaction.message.reply(reacted)

@bot.command()
async def create_react(ctx):
    await ctx.message.delete()
    emoji = ctx.guild.emojis # 'react' is the name of the custom emoji
    for i in emoji:
        if i.name == "react":
            await i.delete()
    # Create the emoji
    try:
        file_path = "Reactions/reactbot_profile.png"
        with open(file_path, "rb") as img:
            emoji = await ctx.guild.create_custom_emoji(name="react", image=img.read())
            reacted = react_text()
            await ctx.send(f'# Reaction emoji has been created!\n ' + f'# "'+ f'{reacted}' +f'" - {emoji}')

    except discord.HTTPException as e:
        await ctx.send(f"Failed to create emoji: {e}")

@bot.event
async def on_message(message):
    # Ignore the bot's own messages
    if message.author == bot.user:
        return

    # Define the phrase you want to detect
    target_phrase = "overwatch futa"

    # Check if the target phrase is in the message content (case-insensitive)
    if target_phrase.lower() in message.content.lower():
        await message.reply("+ 10 Sean Bucks")
    else:
        await bot.process_commands(message)


bot.run(BOT_TOKEN)