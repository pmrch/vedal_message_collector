import os
import twitchio # type: ignore
import logging

from twitchio.ext import commands # type: ignore
from dotenv import load_dotenv
from typing import List
from datetime import datetime
from utils.helper_functions import setup_logger


# Load environment variables
load_dotenv()

# Preconfigure logging
today: str = datetime.today().strftime("%Y-%m-%d")
os.makedirs("data/logs/twitch_bot_logs", exist_ok=True)

twitch_logger = setup_logger("twitch_bot", f"data/logs/twitch_bot_logs/{today}.log")

class Bot(commands.Bot):
    def __init__(self, discord_bot, *args, **kwargs):
        # Initialize bot with access token, prefix
        # and a list of channels to join on start...
        ACCESS_TOKEN: str = os.getenv("TWITCH_TOKEN", "")
        prefix: str = "!"
        initial_channels: List[str] = ["vedal987", "yeetzgaming20"]
        
        self.discord_bot = discord_bot
        self.vip_list: List[str] = []
        
        with open("data/vip_users.txt", "rt", encoding="utf-8", errors="ignore") as file:
            lines: List[str] = file.readlines()
            for line in lines:
                self.vip_list.append(line.strip().lower())
            
        print(self.vip_list)
        
        super().__init__( # type: ignore
            token=ACCESS_TOKEN,
            prefix=prefix,
            initial_channels=initial_channels
        )
        
    async def event_ready(self):
        twitch_logger.info(f"Successfully logged in as | {self.nick}") # type: ignore
        twitch_logger.info(f"User id is | {self.user_id}")
        
    async def event_message(self, message: twitchio.Message) -> None:
        if message.echo:
            return
        
        if message.author.name and message.author.name.lower() in self.vip_list:
            await self.discord_bot.on_ved_message(message.content, self.discord_bot.channel_id, str(message.author.name.lower()))
            twitch_logger.info("Successfully identified a VIP user message")