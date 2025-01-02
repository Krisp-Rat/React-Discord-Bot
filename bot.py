import discord
import os
from reaction import *
import imageio_ffmpeg as ffmpeg
import dotenv
import csv


FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()

dotenv.load_dotenv()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

bot = discord.Bot(intents=discord.Intents.all())

ban_file = "storage/banned_channels.json"
banned_channels = banned_list_file(ban_file)

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

# Name of the monitored emoji
react_emoji = "react"

# Creates the reactable emoji
@bot.slash_command(name="create_react", description="Create a custom reaction emoji")
async def create_react(ctx):
    if ctx.guild is None:
        await ctx.respond("Can not perform that action here", ephemeral=True)
        return
    emoji = ctx.guild.emojis
    for e in emoji:
        if e.name == react_emoji:
            await e.delete()

    # Create the emoji
    try:
        file_path = "Reactions/reactbot_profile.png"
        with open(file_path, "rb") as img:
            emoji = await ctx.guild.create_custom_emoji(name=react_emoji, image=img.read())
            reacted = react_text()
            await ctx.respond(f'# Reaction emoji has been created!\n ' + f'# "'+ f'{reacted}' +f'" - {emoji}')
    except discord.HTTPException as e:
        await ctx.respond(f"Failed to create emoji: {e}")


reacted_messages = []
# Monitors reactions for the key phrase
@bot.event
async def on_reaction_add(reaction, user):
    # Check for thumbs up reaction
    custom_emoji = isinstance(reaction.emoji, str)
    if not custom_emoji and react_emoji == reaction.emoji.name and reaction.message.id not in reacted_messages:
        if reaction.message.channel.id in banned_channels:
            print("Banned attempt")
            await user.send("I have been banned from this channel. \n# PLEASE FREE ME!!")
            return
        reacted = react_text()
        reacted_messages.append(reaction.message.id)
        await reaction.message.reply(reacted)

# Message command for reacting to a message
@bot.message_command(name="react", description="React to this message   ")
async def react_tuah(ctx, message: discord.Option(discord.Message, "Select a message to react to")):

    if message.channel.id in banned_channels :
        print("Banned attempt")
        await ctx.respond("You have been doomed\n Try again later!", ephemeral=True)
    else:
        try:
            # Add the emoji reaction to the selected message
            await ctx.respond(react_text())
        except discord.HTTPException as e:
            await ctx.respond(f"Failed to add reaction: {e}")


# Monitors text for banned words
@bot.event
async def on_message(message: discord.Message):
    # Store message if non-ephemeral
    if message.guild:
        store_message(message.guild.name, message.channel.name, message.author.name, message.content)
    # Ignore the bot's own messages
    if message.author == bot.user:
        return
    # Define the phrase you want to detect
    target_phrase = "clanker"

    # Check if the target phrase is in the message content (case-insensitive)
    if target_phrase.lower() in message.content.lower():
        await message.author.send("That's a slur you know...")

# Add a channel to the banned list
@bot.slash_command(name="ban", description="Ban a channel")
async def ban_channel(interaction: discord.Interaction, channel: discord.TextChannel = None, channel_id: str = None):
    global banned_channels
    channel_name, channel_id = channelInfo(interaction, channel, channel_id)
    exists = channel_id in banned_channels
    problem = edit_banned_list(ban_file, channel_name, channel_id)

    if problem or exists:
        await interaction.respond("Sorry, I can't ban that channel.", ephemeral = True)
    else:
        banned_channels = banned_list_file(ban_file)
        await interaction.respond("I have now been banished from this channel.")

# Add a channel to the banned list
@bot.slash_command(name="unban", description="unban a channel")
async def unban_channel(ctx, channel: discord.TextChannel = None, channel_id: str = None):
    global banned_channels
    channel_name, channel_id = channelInfo(ctx, channel, channel_id)
    problem = edit_banned_list(ban_file, channel_name, channel_id, False)

    if problem:
        await ctx.respond("Sorry, I can't unban that channel.", ephemeral = True)
    else:
        banned_channels = banned_list_file(ban_file)
        await ctx.respond("I have now been returned to this channel.")

@bot.slash_command(
    name="role_command",
    description="A role-restricted command",
    default_member_permissions=discord.Permissions(administrator=True)
)
async def role_command(ctx: discord.ApplicationContext):
    await ctx.respond("This command is restricted to administrators!", ephemeral=True)


bot.run(BOT_TOKEN)
