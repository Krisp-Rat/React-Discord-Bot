import asyncio
import os

from discord.ext import commands
from discord import app_commands
import dotenv

# from openai import OpenAI
# client = OpenAI()

from reaction import *

dotenv.load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), owner_id=419636034037481472)

banned_channels = banned_list_file(os.getenv("BAN_FILE"))

# Name of the monitored emoji
react_emoji = os.getenv("REACT_EMOJI")


admin_access = [discord.Object(id=507666860427313162)]

@bot.event
async def on_ready():
    await bot.tree.sync()
    for server in admin_access:
        await bot.tree.sync(guild=server)
    # await bot.tree.sync(guild=discord.Object(id=629070806193799198)) # Ramen server sync
    print(f"{bot.user} is ready and online!")


# Message command for reacting to a message
@bot.tree.context_menu(name="react")
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@app_commands.allowed_installs(guilds=True, users=True)
async def react_tuah(ctx: discord.interactions, message: discord.Message):
    # React to a message
    # optional enable tts?
    if str(message.channel.id) in banned_channels :
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

            store_message("Message Command", ctx.user, message.author.name, message.content, message.attachments)
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



@bot.tree.command(name="role_command_test", description="Admin only command")
async def role_command(ctx: discord.interactions):
    emoji = "<:poop_deli:1324630414442365052>"
    print(f"{ctx.user} got Pepsi Dogged")
    await ctx.response.send_message(f"Here is pepsi dog: {emoji}", ephemeral = True)


async def loadCogs():
    """Load all cogs."""
    try:
        for cog in os.listdir("Cogs"):
            if cog != "__pycache__":
                await bot.load_extension(f"Cogs.{cog[:-3]}")  # Add your cogs here
                print(f"Cog {cog[:-3]} loaded successfully.")
    except Exception as e:
        print(f"Error loading cog: {e}")

    # Set TextChannel cog
    cog = bot.get_cog("TextChannel")
    cog.set(react_emoji, banned_channels)


async def main():
    async with bot:  # Graceful startup and cleanup
        await loadCogs()
        await bot.start(str(os.getenv("BOT_TOKEN")))

asyncio.run(main())

