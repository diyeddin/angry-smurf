import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('../.env')

logger = logging.getLogger(__name__)

def validate_config():
    """Validate required environment variables and their types"""
    required_vars = ["DISCORD_TOKEN", "CHANNEL_ID", "GROQ_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.error(f"Missing required environment variables: {missing}")
        raise ValueError(f"Missing required environment variables: {missing}")
    
    try:
        int(os.getenv("CHANNEL_ID"))
    except (ValueError, TypeError):
        raise ValueError("CHANNEL_ID must be a valid integer")
    
    logger.info("Configuration validated successfully")

class Config:
    """Bot configuration settings"""
    
    def __init__(self):
        validate_config()
        
        # Discord settings
        self.DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
        self.CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
        
        # Testing mode settings
        self.TESTING_MODE = os.getenv("TESTING_MODE", "false").lower() == "true"
        self.TEST_CHANNEL_ID = int(os.getenv("TEST_CHANNEL_ID", self.CHANNEL_ID))
        
        # Use test channel if in testing mode
        self.ACTIVE_CHANNEL_ID = self.TEST_CHANNEL_ID if self.TESTING_MODE else self.CHANNEL_ID
        
        # Groq API settings
        self.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        self.GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        # Bot behavior settings (with testing mode overrides)
        if self.TESTING_MODE:
            # More aggressive settings for testing
            self.COOLDOWN = int(os.getenv("TEST_COOLDOWN", 30))  # 30 seconds instead of 10 minutes
            self.USER_COOLDOWN = int(os.getenv("TEST_USER_COOLDOWN", 10))  # 10 seconds instead of 1 minute
            self.BASE_CHANCE = float(os.getenv("TEST_BASE_CHANCE", 0.1))  # 10% instead of 0.05%
            self.SCALE_FACTOR = float(os.getenv("TEST_SCALE_FACTOR", 0.05))  # 5% per message
            self.MAX_CHANCE = float(os.getenv("TEST_MAX_CHANCE", 1.0))  # 100% cap for testing
            logger.info("🧪 TESTING MODE ENABLED - Using aggressive trigger settings")
        else:
            # Normal production settings
            self.COOLDOWN = int(os.getenv("COOLDOWN", 300))
            self.USER_COOLDOWN = int(os.getenv("USER_COOLDOWN", 60))
            self.BASE_CHANCE = float(os.getenv("BASE_CHANCE", 0.001))
            self.SCALE_FACTOR = float(os.getenv("SCALE_FACTOR", 0.0005))
            self.MAX_CHANCE = float(os.getenv("MAX_CHANCE", 0.10))  # 10% cap for production
        
        self.CLEANUP_INTERVAL = int(os.getenv("CLEANUP_INTERVAL", 3600))
        
        mode_str = "TESTING" if self.TESTING_MODE else "PRODUCTION"
        logger.info(f"Config loaded - Mode: {mode_str}, Channel: {self.ACTIVE_CHANNEL_ID}, Cooldown: {self.COOLDOWN}s")