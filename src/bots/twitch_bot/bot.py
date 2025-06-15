import os
import twitchio # type: ignore
import logging

from twitchio.ext import commands # type: ignore
from dotenv import load_dotenv
from typing import List
from datetime import datetime


# Load environment variables
load_dotenv()

# Preconfigure logging
today: str = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
os.makedirs("data/logs/twitch_bot_logs", exist_ok=True)


class Bot(commands.Bot):
    def __init__(self, discord_bot, *args, **kwargs):
        logfile: str = f"data/logs/twitch_bot_logs/{today}.log"
        logging.basicConfig(
            filename=logfile,
            filemode="a",
            level=logging.DEBUG,
            encoding="utf-8"
        )
        
        # Initialize bot with access token, prefix
        # and a list of channels to join on start...
        ACCESS_TOKEN: str = os.getenv("TWITCH_TOKEN", "")
        prefix: str = "!"
        initial_channels: List[str] = ["vedal987", "yeetzgaming20"]
        
        self.discord_bot = discord_bot
        
        super().__init__( # type: ignore
            token=ACCESS_TOKEN,
            prefix=prefix,
            initial_channels=initial_channels
        )
        
    async def event_ready(self):
        logging.info(f"Successfully logged in as | {self.nick}") # type: ignore
        logging.info(f"User id is | {self.user_id}")
        
    async def event_message(self, message: twitchio.Message) -> None:
        if message.echo:
            return
        
        if message.author.name and message.author.name.lower() == "vedal987":
            await self.discord_bot.on_ved_message(message.content, self.discord_bot.channel_id)