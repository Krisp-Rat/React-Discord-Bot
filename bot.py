import discord
import os
from reaction import *
import imageio_ffmpeg as ffmpeg
import dotenv


FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()

dotenv.load_dotenv()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

@bot.slash_command(name="saysomething", description="Say hello to the bot")
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")


@bot.slash_command(name="join", description="Join a voice channel")
async def join(ctx: discord.ApplicationContext):
    # Check if the user is in a voice channel
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        # Connect to the channel
        await channel.connect()
        await ctx.respond("Connected to your voice channel!", ephemeral=True)
    else:
        await ctx.respond("You need to be in a voice channel for me to join!", ephemeral=True)

@bot.slash_command(name="leave", description="Leave the voice channel")
async def leave(ctx):
    # Check if the bot is in a voice channel
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.respond("Disconnected from the voice channel.", ephemeral=True)
    else:
        await ctx.respond("I'm not in a voice channel!", ephemeral=True)

@bot.slash_command(name="react", description="Play a reaction sound in the voice channel")
async def react(ctx):
    if not ctx.voice_client:
        await ctx.respond("I'm not connected to a voice channel! Use /join to connect me.", ephemeral=True)
        return

    try:
        # Ensure the bot is connected to a voice channel
        vc = ctx.voice_client

        # Prepare the audio source using FFmpeg
        sound_url = grab_reaction()
        audio_source = discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=f"Reactions/GrabBag/{sound_url}")

        if not vc.is_playing():
            vc.play(audio_source, after=lambda e: print(f"Error: {e}") if e else None)
            await ctx.respond("I love you", ephemeral=True)
        else:
            await ctx.respond("Already playing audio. Please wait until it's finished.", ephemeral=True)
    except Exception as e:
        await ctx.respond(f"An error occurred: {e}", ephemeral=True)

@bot.slash_command(name="create_react", description="Create a custom reaction emoji")
async def create_react(ctx):
    emoji = ctx.guild.emojis
    for e in emoji:
        if e.name == "react":
            await e.delete()

    # Create the emoji
    try:
        file_path = "Reactions/reactbot_profile.png"
        with open(file_path, "rb") as img:
            emoji = await ctx.guild.create_custom_emoji(name="react", image=img.read())
            reacted = react_text()
            await ctx.respond(f'# Reaction emoji has been created!\n ' + f'# "'+ f'{reacted}' +f'" - {emoji}')
    except discord.HTTPException as e:
        await ctx.respond(f"Failed to create emoji: {e}")

reacted_messages = []
@bot.event
async def on_reaction_add(reaction, user):
    # Check for thumbs up reaction
    if "react" == reaction.emoji.name and reaction.message.id not in reacted_messages:
        reacted = react_text()
        reacted_messages.append(reaction.message.id)
        await reaction.message.reply(reacted)

@bot.slash_command(name="react_tuah", description="React on that thang")
async def react_tuah(ctx, message: discord.Option(discord.Message, "Select a message to react to")):
    try:
        # Add the emoji reaction to the selected message
        catch_phrase = react_text()
        await ctx.respond(f"Reacted to {message}!")
    except discord.HTTPException as e:
        await ctx.respond(f"Failed to add reaction: {e}")

# @bot.event
# async def on_message(message):
#     # Ignore the bot's own messages
#     if message.author == bot.user:
#         return
#
#     # Define the phrase you want to detect
#     target_phrase = "overwatch futa"
#
#     # Check if the target phrase is in the message content (case-insensitive)
#     if target_phrase.lower() in message.content.lower():
#         await message.reply("+ 10 Sean Bucks")

bot.run(BOT_TOKEN)
