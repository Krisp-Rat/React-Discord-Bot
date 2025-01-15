import discord
from discord.ext import commands
from discord import app_commands
from reaction import store_message

admin_access = [discord.Object(id=507666860427313162)]

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Speak through the React bot
    @app_commands.command(name="speak", description="Speak through me")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    @app_commands.guilds(*admin_access)
    async def speak_through_me(self, ctx, channel_id: str, message_id: str, reply_content: str):
        """Reply to a specific message given its channel ID and message ID."""
        channel_id = int(channel_id)
        message_id = int(message_id)
        try:
            # Fetch the channel
            channel = await self.bot.fetch_channel(channel_id)
            if not isinstance(channel, (discord.TextChannel, discord.DMChannel)):
                await ctx.response.send_message("Invalid channel type. Make sure it's a text or DM channel.", ephemeral = True)
                return

            # Fetch the message
            message = await channel.fetch_message(message_id)
            # Reply to the message
            await message.reply(reply_content)
            await ctx.response.send_message(f"Replied to the message: {message.content}", ephemeral = True)

        except discord.NotFound:
            await ctx.response.send_message("Message or channel not found.", ephemeral = True)
        except discord.Forbidden:
            await ctx.response.send_message("I don't have permission to access that message or channel.", ephemeral = True)
        except discord.HTTPException as e:
            await ctx.response.send_message(f"An error occurred: {e}", ephemeral = True)

    # Monitors text for banned words
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):

        # Store message if non-ephemeral
        if message.guild:
            store_message(message.guild.name, message.channel.name, message.author.name, message.content,
                          message.attachments)

        # Ignore the bot's own messages
        if message.author == self.bot.user:
            return

        # Define the phrase you want to detect
        target_phrase = "clanker"
        # Check if the target phrase is in the message content (case-insensitive)
        if target_phrase.lower() in message.content.lower():
            await message.author.send("That's a slur you know...")

        await self.bot.process_commands(message)

async def setup(bot):
    """Setup function to load the cog."""
    await bot.add_cog(Admin(bot))
