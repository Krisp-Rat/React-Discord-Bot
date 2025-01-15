import discord
from discord.ext import commands
from sympy.unify.usympy import basic_new_legal

from reaction import react_text


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

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Triggered when a reaction is added to a message."""
        print("listened in")
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
