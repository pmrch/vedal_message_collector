# -*- coding: utf-8 -*-

# Full imports
import discord
import re
import os

# Partial imports
from datetime import datetime
from discord.ext.commands import Context, Bot # type: ignore
from discord.ext import commands
from utils.helper_functions import setup_logger

# Set up logging
os.makedirs("data/logs/discord_bot_logs", exist_ok=True)
now: datetime = datetime.today()

logfile: str = f"data/logs/discord_bot_logs/{now.strftime('%Y-%m-%d')}.log"
discord_logger = setup_logger("discord_log", logfile)

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        
    @commands.command()
    async def ping(self, ctx: Context[Bot]):
        await ctx.send(f"Latency: {round(self.bot.latency * 1000, 3)}ms")
        discord_logger.info("A user issued the ping command")

class DiscordBot(Bot):
    def __init__(self, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        
    async def on_ready(self):
        if self.user:
            discord_logger.info(f"Successfully logged in as {self.user.name}")
        else:
            discord_logger.warning("Failed to log in as user")
            
    async def on_message(self, message: discord.Message):
        if self.user is None:
            discord_logger.warning("Bot user is None in on_message")
            return
        
        if not message.author or message.author.id == self.user.id:
            # Ignore messages from the bot or with no author
            return
        
        # Catch any command sent by user(s)    
        await self.process_commands(message)
    
    async def on_ved_message(self, message_content: str, channel_id: int, message_author: str, message_channel: str):
        channel = self.get_channel(channel_id)
        pattern = re.compile(r'mewed for mini OwO\s*$', re.IGNORECASE)
        
        if channel and isinstance(channel, discord.abc.Messageable):
            if not pattern.search(message_content):
                await channel.send(f"Channel: {message_channel} | {message_author}: {message_content}")
            else:
                return
        
        else:
            discord_logger.error("Can't send message: Invalid channel or missing permissions.")

def create_bot(token: str, channel_id: int) -> Bot:
    # Configure discord intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    # Create instance of Client
    bot = DiscordBot(channel_id=channel_id, command_prefix="!", intents=intents)
    return bot