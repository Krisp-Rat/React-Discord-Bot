import discord
from discord.ext import commands
from discord import app_commands

from reaction import react_text, store_message


class TextChannel(commands.Cog):
    """Cog to monitor and respond to specific reactions."""

    def __init__(self, bot):
        self.bot = bot
        self.react_emoji = ""
        self.banned_channels = []
        self.reacted_messages = []  # Keep track of reacted message IDs

    # Update key global values
    def set(self, emoji = None, banned_channels = None):
        if emoji:
            self.react_emoji = emoji
        if banned_channels:
            self.banned_channels = banned_channels

    # Creates the reactable emoji
    @app_commands.command(name="create_react", description="Create a custom reaction emoji")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def create_react(self, ctx):
        if ctx.guild is None:
            await ctx.response.send_message("Can not perform that action here", ephemeral=True)
            return
        emoji = ctx.guild.emojis
        for e in emoji:
            if e.name == self.react_emoji:
                await e.delete()

        # Create the emoji
        try:
            file_path = "Reactions/reactbot_profile.png"
            with open(file_path, "rb") as img:
                emoji = await ctx.guild.create_custom_emoji(name=self.react_emoji, image=img.read())
                reacted = react_text()
                await ctx.response.send_message(
                    f'# Reaction emoji has been created!\n ' + f'# "' + f'{reacted}' + f'" - {emoji}')
        except discord.HTTPException as e:
            await ctx.response.send_message(f"Failed to create emoji: {e}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Triggered when a reaction is added to a message."""
        # Check if the reaction is a standard emoji or custom emoji
        custom_emoji = isinstance(reaction.emoji, str)

        # Check for the reaction criteria
        if not custom_emoji and reaction.emoji.name == self.react_emoji and reaction.message.id not in self.reacted_messages:
            if reaction.message.channel.id in self.banned_channels:
                print("Banned attempt")
                try:
                    await user.send("I have been banned from this channel. \n# PLEASE FREE ME!!")
                except discord.Forbidden:
                    print(f"Could not send a DM to {user}.")
                return

            # Respond to the reaction
            reacted_text = react_text()  # Call your custom function
            self.reacted_messages.append(reaction.message.id)  # Add to reacted list
            await reaction.message.reply(reacted_text)


async def setup(bot):
    """Setup function to load the cog."""
    await bot.add_cog(TextChannel(bot))
