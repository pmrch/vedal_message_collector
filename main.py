import os
import asyncio

from dotenv import load_dotenv
from src.bots.discord_bot.bot import create_bot
from src.bots.twitch_bot.bot import Bot


# Load environment variables and set API keys
load_dotenv()

# Run main loop
async def main():
    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
    #TWITCH_TOKEN: str = os.getenv("TWITCH_TOKEN", "")
    DISCORD_CHANNEL_ID: int = int(os.getenv("DISCORD_CHANNEL_ID", ""))
    
    # Create bots
    discord_bot = create_bot(DISCORD_TOKEN, DISCORD_CHANNEL_ID)
    twitch_bot = Bot(discord_bot=discord_bot)
    
    # Run both
    
    await asyncio.gather(
        discord_bot.start(DISCORD_TOKEN),
        twitch_bot.start()
    )
    
if __name__ == "__main__":
    asyncio.run(main())