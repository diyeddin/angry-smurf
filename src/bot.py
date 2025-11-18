import discord
import logging
import asyncio
import random

from config import Config
from llm_client import GeminiClient
from message_tracker import MessageTracker

# --------------------------
# Logging setup
# --------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --------------------------
# Initialize components
# --------------------------
config = Config()
gemini_client = GeminiClient(config)
tracker = MessageTracker(config)

# --------------------------
# Discord bot setup
# --------------------------
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logger.info(f"Bot logged in as {client.user}")
    logger.info(f"Active Channel: {config.ACTIVE_CHANNEL_ID}")
    logger.info(f"Using Model: {config.GEMINI_MODEL}")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != config.ACTIVE_CHANNEL_ID:
        return

    # Check if bot is mentioned
    is_mention = client.user in message.mentions
    
    # Ask the Social Engine if we should trigger
    result = tracker.process_message(message.author.id, message.content, is_mention)
    
    if result['trigger']:
        # Prepare context for LLM
        context_note = ""
        if result['is_burst']:
            context_note = "IMPORTANT: You are currently in a heated argument with this user. They just replied to you. Be sharper and faster."
        
        # 1. Human Latency: "Reading" the message
        # If it's a burst argument, read fast. If random trigger, read slow.
        read_time = random.uniform(0.5, 1.5) if result['is_burst'] else random.uniform(config.READING_DELAY_MIN, config.READING_DELAY_MAX)
        await asyncio.sleep(read_time)
        
        # 2. Generate text (while "thinking")
        reply_text = gemini_client.generate_angry_reply(message.author.mention, message.content, context_note)
        
        if not reply_text: 
            return

        # 3. Human Latency: "Typing" the message
        # Calculate typing time based on length
        typing_duration = len(reply_text) * config.TYPING_SPEED
        # Cap typing time to 10 seconds max to avoiding hanging too long
        typing_duration = min(typing_duration, 10.0)
        
        try:
            async with message.channel.typing():
                await asyncio.sleep(typing_duration)
                await message.channel.send(reply_text)
                logger.info(f"Sent reply to {message.author}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")

if __name__ == "__main__":
    client.run(config.DISCORD_TOKEN)