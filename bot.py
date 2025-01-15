import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import dotenv
import imageio_ffmpeg as ffmpeg
from datetime import datetime

# from openai import OpenAI
# client = OpenAI()

from reaction import *

FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()

dotenv.load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), owner_id=419636034037481472)

ban_file = "Storage/banned_channels.json"
banned_channels = banned_list_file(ban_file)

admin_access = [discord.Object(id=507666860427313162)]

# Name of the monitored emoji
react_emoji = "react"



@bot.event
async def on_ready():
    await bot.tree.sync()
    for server in admin_access:
        await bot.tree.sync(guild=server)
    # await bot.tree.sync(guild=discord.Object(id=629070806193799198)) # Ramen server sync
    print(f"{bot.user} is ready and online!")

@bot.tree.command(name="join", description="Join a voice channel")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def join(ctx, vc: discord.VoiceChannel = None, vc_id: str = None):
    # Check if the user is in a voice channel
    if not vc:
        try:
            if vc_id:
                vc_id = int(vc_id)
                vc = await bot.fetch_channel(vc_id)
            else:
                vc = ctx.user.voice.channel
        except Exception as e:
            await ctx.response.send_message("Must be in a VC or specify voice channel", ephemeral=True)
            return

    # Check if the bot is already connected to a voice channel
    try:
        voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        if voice_client:
            await voice_client.disconnect(force=True)
            await vc.connect()# Move bot to the new channel
            await ctx.response.send_message(f"Moved to {vc.name}", ephemeral=True)
        else:
            await vc.connect()  # Connect the bot to the provided channel
            await ctx.response.send_message(f"Connected to {vc.name}", ephemeral=True)

    except Exception as e:
        await ctx.response.send_message(f"Could not join {vc.name}", ephemeral=True)
        return

@bot.tree.command(name="leave", description="Leave the voice channel")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def leave(ctx):
    # Check if the bot is in a voice channel
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client:
        await voice_client.disconnect()
        await ctx.response.send_message("Disconnected from the voice channel.", ephemeral=True)
    else:
        await ctx.response.send_message("I'm not in a voice channel!", ephemeral=True)

@bot.tree.command(name="react", description="Play a reaction sound in the voice channel")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def react(ctx):
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice_client:
        await ctx.response.send_message("I'm not connected to a voice channel! Use /join to connect me.", ephemeral=True)
        return

    try:
        # Ensure the bot is connected to a voice channel

        # Prepare the audio source using FFmpeg
        sound_url = grab_reaction()
        audio_source = discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=f"Reactions/GrabBag/{sound_url}")

        if not voice_client.is_playing():
            voice_client.play(audio_source, after=lambda e: print(f"Error: {e}") if e else None)
            await ctx.response.send_message("I love you", ephemeral=True)
        else:
            await ctx.response.send_message("Already playing audio. Please wait until it's finished.", ephemeral=True)
    except Exception as e:
        await ctx.response.send_message(f"An error occurred: {e}", ephemeral=True)


# Creates the reactable emoji
@bot.tree.command(name="create_react", description="Create a custom reaction emoji")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def create_react(ctx):
    if ctx.guild is None:
        await ctx.response.send_message("Can not perform that action here", ephemeral=True)
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
            await ctx.response.send_message(f'# Reaction emoji has been created!\n ' + f'# "'+ f'{reacted}' +f'" - {emoji}')
    except discord.HTTPException as e:
        await ctx.response.send_message(f"Failed to create emoji: {e}")


# Message command for reacting to a message
@bot.tree.context_menu(name="react")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def react_tuah(ctx: discord.interactions, message: discord.Message):
    # React to a message
    # optional enable tts?
    if message.channel.id in banned_channels :
        print("Banned attempt")
        await ctx.response.send_message("You have been doomed\n Try again later!", ephemeral=True)
    else:
        try:
            react_phrase = react_text()
            # If this phrase is chosen then return the current time
            if react_phrase == "Tell the current time":
                if random.randint(0, 1) < .5:
                    time = datetime.now().strftime("%H:%M %p")  # Current time in readable format
                    react_phrase = f"The current time is {time}"
            if ctx.guild and ctx.guild.name != "":
                channel = "Server"
                await message.reply(react_phrase)
                await ctx.response.send_message("Thank you for your service", ephemeral=True)
            else:
                channel = "Server" if ctx.guild and ctx.guild.name == "" else "DM"
                await ctx.response.send_message(react_phrase)

            store_message("Message Command", ctx.user, message.author.name, message.content, [])
            store_message("Message Command", channel, "React Bot", react_phrase, [])
        except discord.HTTPException as e:
            await ctx.response.send_message(f"Failed to add reaction: {e}", ephemeral=True)

@bot.tree.context_menu(name="fish_react")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=False)
async def fish_react(ctx: discord.interactions, message: discord.Message):
    EMOJI_IDS = [1326703066384306267, 1326699914347937863, 1326702920804208711, 1326703023975825471]
    try:
        # React with each emoji
        for emoji_id in EMOJI_IDS:
            emoji = f"<:FISH:{emoji_id}>"
            if emoji:
                await message.add_reaction(emoji)
            else:
                await ctx.response.send_message(f"Could not find emoji with ID: {emoji_id}", ephemeral=True)
                return
        await ctx.response.send_message("You fish reacted!", ephemeral=True)

    except discord.Forbidden:
        await ctx.response.send_message("I don't have permission to add reactions in this channel.", ephemeral=True)
    except discord.HTTPException as e:
        await ctx.response.send_message(f"An error occurred: {e}", ephemeral=True)

# Monitors text for banned words
@bot.event
async def on_message(message: discord.Message):
    # Store message if non-ephemeral
    if message.guild:
        store_message(message.guild.name, message.channel.name, message.author.name, message.content, message.attachments)
    # Ignore the bot's own messages
    if message.author == bot.user:
        return


    # Define the phrase you want to detect
    target_phrase = "clanker"
    # Check if the target phrase is in the message content (case-insensitive)
    if target_phrase.lower() in message.content.lower():
        await message.author.send("That's a slur you know...")

    await bot.process_commands(message)




# Speak through the React bot
@bot.tree.command(name="speak", description="Speak through me")
@app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.guilds(*admin_access)
async def speak_through_me(ctx, channel_id: str, message_id: str, reply_content: str):
    """Reply to a specific message given its channel ID and message ID."""
    channel_id = int(channel_id)
    message_id = int(message_id)
    try:
        # Fetch the channel
        channel = await bot.fetch_channel(channel_id)
        print("Got channel: ", channel.name)
        if not isinstance(channel, (discord.TextChannel, discord.DMChannel)):
            await ctx.response.send_message("Invalid channel type. Make sure it's a text or DM channel.", ephemeral = True)
            return


        # Fetch the message
        message = await channel.fetch_message(message_id)
        print("Got message: ", message.content)
        # Reply to the message
        await message.reply(reply_content)
        await ctx.response.send_message(f"Replied to the message: {message.content}", ephemeral = True)
    except discord.NotFound:
        await ctx.response.send_message("Message or channel not found.", ephemeral = True)
    except discord.Forbidden:
        await ctx.response.send_message("I don't have permission to access that message or channel.", ephemeral = True)
    except discord.HTTPException as e:
        await ctx.response.send_message(f"An error occurred: {e}", ephemeral = True)



# Add a channel to the banned list
@bot.tree.command(name="ban", description="Ban a channel")
@app_commands.guilds(*admin_access)
async def ban_channel(interaction: discord.interactions, channel: discord.TextChannel = None, channel_id: str = None):
    global banned_channels
    channel_name, channel_id = await channelInfo(interaction, bot, channel, channel_id)
    exists = channel_id in banned_channels
    problem = edit_banned_list(ban_file, channel_name, channel_id)

    if problem or exists:
        await interaction.response.send_message(f"Sorry, I can't ban: {channel_name}", ephemeral = True)
    else:
        banned_channels = banned_list_file(ban_file)
        await interaction.response.send_message(f"I have now been banished from: {channel_name}")


# Add a channel to the banned list
@bot.tree.command(name="unban", description="unban a channel")
@app_commands.guilds(*admin_access)
async def unban_channel(ctx, channel: discord.TextChannel = None, channel_id: str = None):
    global banned_channels
    channel_name, channel_id = await channelInfo(ctx, bot, channel, channel_id)
    exists = channel_id in banned_channels
    problem = edit_banned_list(ban_file, channel_name, channel_id, False)

    if problem or not exists:
        await ctx.response.send_message(f"Sorry, I can't unban: {channel_name}", ephemeral = True)
    else:
        banned_channels = banned_list_file(ban_file)
        await ctx.response.send_message(f"I have now been returned to: {channel_name}")

@bot.tree.command(name="role_command_test", description="Admin only command")
async def role_command(ctx: discord.interactions):
    emoji = "<:poop_deli:1324630414442365052>"
    print(f"{ctx.user} got Pepsi Dogged")
    await ctx.response.send_message(f"Here is pepsi dog: {emoji}", ephemeral = True)


async def loadCogs():
    """Load all cogs."""
    try:
        #for cog in os.listdir("cogs"):
            await bot.load_extension("Cogs.TextChannel")  # Add your cogs here
            print("Cog 'TextChannel;' loaded successfully.")
    except Exception as e:
        print(f"Error loading cog: {e}")

    # Set TextChannel cog
    cog = bot.get_cog("TextChannel")
    cog.set(react_emoji, banned_channels)


async def main():
    async with bot:  # Graceful startup and cleanup
        await loadCogs()
        await bot.start(BOT_TOKEN)

asyncio.run(main())

