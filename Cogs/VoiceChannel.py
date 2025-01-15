import discord
from discord.ext import commands
from discord import app_commands

class VoiceChannel(commands.Cog):
    """General bot commands."""

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="join", description="Join a voice channel")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def join(self, ctx, vc: discord.VoiceChannel = None, vc_id: str = None):
        # Check if the user is in a voice channel
        if not vc:
            try:
                if vc_id:
                    vc_id = int(vc_id)
                    vc = await self.bot.fetch_channel(vc_id)
                else:
                    vc = ctx.user.voice.channel
            except Exception as e:
                await ctx.response.send_message("Must be in a VC or specify voice channel", ephemeral=True)
                return

        # Check if the bot is already connected to a voice channel
        try:
            voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
            if voice_client:
                await voice_client.disconnect(force=True)
                await vc.connect()  # Move bot to the new channel
                await ctx.response.send_message(f"Moved to {vc.name}", ephemeral=True)
            else:
                await vc.connect()  # Connect the bot to the provided channel
                await ctx.response.send_message(f"Connected to {vc.name}", ephemeral=True)

        except Exception as e:
            await ctx.response.send_message(f"Could not join {vc.name}", ephemeral=True)
            return


    async def cog_load(self):
        """Register commands to the bot's app command tree."""
        self.bot.tree.add_command(self.join)


async def setup(bot):
    await bot.add_cog(VoiceChannel(bot))