import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv('../.env')

logger = logging.getLogger(__name__)

def validate_config():
    """Validate required environment variables"""
    required_vars = ["DISCORD_TOKEN", "CHANNEL_ID", "GEMINI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise ValueError(f"Missing required environment variables: {missing}")
    try:
        int(os.getenv("CHANNEL_ID"))
    except (ValueError, TypeError):
        raise ValueError("CHANNEL_ID must be a valid integer")

class Config:
    """Bot configuration settings"""
    
    def __init__(self):
        validate_config()
        
        # Discord settings
        self.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        self.CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
        
        # Testing mode
        self.TESTING_MODE = os.getenv("TESTING_MODE", "false").lower() == "true"
        self.TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID", self.CHANNEL_ID))
        self.ACTIVE_CHANNEL_ID = self.TEST_CHANNEL_ID if self.TESTING_MODE else self.CHANNEL_ID
        
        # Google Gemini Settings
        self.GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        # Using 1.5 Flash as the current standard for speed (2.5/2.0 are usually experimental tags)
        # You can change this string in .env to 'gemini-2.0-flash-exp' if you have access
        self.GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        
        # Social Engine Settings
        self.MOOD_SWITCH_INTERVAL = 7200  # Change mood every 2 hours
        self.BEEF_DECAY_INTERVAL = 86400  # Reduce beef score every 24 hours
        
        # Typing Simulation
        self.TYPING_SPEED = 0.05  # Seconds per character to type
        self.READING_DELAY_MIN = 1.0
        self.READING_DELAY_MAX = 3.0

        # Log configuration
        mode_str = "TESTING" if self.TESTING_MODE else "PRODUCTION"
        logger.info(f"Config loaded - Mode: {mode_str}, Model: {self.GEMINI_MODEL}")