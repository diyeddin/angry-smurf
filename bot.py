import discord
import logging

from config import Config
from llm_client import GroqClient
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
groq_client = GroqClient(config.GROQ_API_KEY, config.GROQ_MODEL)
message_tracker = MessageTracker(config)

# --------------------------
# Discord bot setup
# --------------------------
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# --------------------------
# Bot events
# --------------------------
@client.event
async def on_ready():
    logger.info(f"Bot logged in as {client.user}")
    logger.info(f"Monitoring channel ID: {config.ACTIVE_CHANNEL_ID}")
    logger.info(f"Global cooldown: {config.COOLDOWN}s, User cooldown: {config.USER_COOLDOWN}s")
    if config.TESTING_MODE:
        logger.info("🧪 Bot running in TESTING MODE with aggressive trigger settings")
    
    # Create health check file for Docker
    try:
        with open("/tmp/bot_health", "w") as f:
            f.write("healthy")
    except Exception:
        pass  # Ignore if we can't write (non-Docker environment)

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.channel.id != config.ACTIVE_CHANNEL_ID:
        return

    user_id = message.author.id
    
    # Check if bot was mentioned - immediate response
    bot_mentioned = client.user in message.mentions
    
    # Check if bot should respond (either by mention or probability)
    should_respond, chance = message_tracker.should_respond(user_id, force_respond=bot_mentioned)
    
    if should_respond:
        trigger_reason = "mention" if bot_mentioned else f"probability ({chance:.4f})"
        logger.info(f"Triggered response for {message.author} - {trigger_reason}")
        
        # Generate LLM reply
        reply = groq_client.generate_angry_reply(message.author.mention, message.content)

        # Safety check for empty messages
        if not reply or not reply.strip():
            logger.error("Generated reply is empty, skipping message send")
            return

        try:
            await message.channel.send(reply)
            logger.info(f"Sent angry reply to {message.author}")
        except discord.errors.DiscordException as e:
            logger.error(f"Failed to send message: {e}")

# --------------------------
# Run bot
# --------------------------
if __name__ == "__main__":
    client.run(config.DISCORD_TOKEN)