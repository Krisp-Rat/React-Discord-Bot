import discord
from discord.ext import commands
from discord import app_commands
from reaction import grab_reaction
import imageio_ffmpeg as ffmpeg

class VoiceChannel(commands.Cog):
    """General bot commands."""

    def __init__(self, bot):
        self.bot = bot
        self.FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()

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


    @app_commands.command(name="leave", description="Leave the voice channel")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def leave(self, ctx):
        # Check if the bot is in a voice channel
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client:
            await voice_client.disconnect()
            await ctx.response.send_message("Disconnected from the voice channel.", ephemeral=True)
        else:
            await ctx.response.send_message("I'm not in a voice channel!", ephemeral=True)

    @app_commands.command(name="react", description="Play a reaction sound in the voice channel")
    @app_commands.allowed_contexts(guilds=True, dms=False, private_channels=True)
    @app_commands.allowed_installs(guilds=True, users=True)
    async def react(self, ctx):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            await ctx.response.send_message("I'm not connected to a voice channel! Use /join to connect me.",
                                            ephemeral=True)
            return

        try:
            # Ensure the bot is connected to a voice channel

            # Prepare the audio source using FFmpeg
            sound_url = grab_reaction()
            audio_source = discord.FFmpegPCMAudio(executable=self.FFMPEG_PATH, source=f"Reactions/GrabBag/{sound_url}")

            if not voice_client.is_playing():
                voice_client.play(audio_source, after=lambda e: print(f"Error: {e}") if e else None)
                await ctx.response.send_message("I love you", ephemeral=True)
            else:
                await ctx.response.send_message("Already playing audio. Please wait until it's finished.",
                                                ephemeral=True)
        except Exception as e:
            await ctx.response.send_message(f"An error occurred: {e}", ephemeral=True)



async def setup(bot):
    await bot.add_cog(VoiceChannel(bot))