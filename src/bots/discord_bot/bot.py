# -*- coding: utf-8 -*-

# Full imports
import discord
import logging
import os

# Partial imports
from datetime import datetime
from discord.ext.commands import Context, Bot, command # type: ignore


class DiscordBot(Bot):
    def __init__(self, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = channel_id
        
        
        # Set up logging
        os.makedirs("data/logs/discord_bot_logs", exist_ok=True)
        now: datetime = datetime.today()
        logfile: str = f"data/logs/discord_bot_logs/{now.strftime('%Y-%m-%d')}.log"

        logging.basicConfig(
            filename=logfile,
            filemode="a",
            level=logging.DEBUG,
            encoding="utf-8"
        )
        
    async def on_ready(self):
        if self.user:
            logging.info(f"Successfully logged in as {self.user.name}")
        else:
            logging.warning("Failed to log in as user")
            
    async def on_message(self, message: discord.Message):
        if self.user is None:
            logging.warning("Bot user is None in on_message")
            return
        
        if not message.author or message.author.id == self.user.id:
            # Ignore messages from the bot or with no author
            return
        
        # Catch any command sent by user(s)    
        await self.process_commands(message)

    async def ping(self, ctx: Context[Bot]):
        if (self.user and ctx.author) and self.user.id != ctx.author.id:
            logging.info(f"{ctx.author.name} executed a ping command")
            await ctx.send(f"Latency: {round(self.latency * 1000, 3)}ms")
        else:
            pass
            
    async def on_ved_message(self, message_content: str, channel_id: int):
        channel = self.get_channel(channel_id)
        if channel and isinstance(channel, discord.abc.Messageable): 
            await channel.send(f"vedal987: {message_content}")
        else:
            logging.error("Can't send message: Invalid channel or missing permissions.")

def create_bot(token: str, channel_id: int) -> Bot:
    # Configure discord intents
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True
    
    # Create instance of Client
    bot = DiscordBot(channel_id=channel_id, command_prefix="!", intents=intents)
    return bot