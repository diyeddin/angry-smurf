import time
import random
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class MessageTracker:
    """Track user messages, cooldowns, and cleanup old data"""
    
    def __init__(self, config):
        self.config = config
        self.last_reply = 0
        self.user_message_counts = defaultdict(int)
        self.user_last_reply = defaultdict(int)
        self.last_cleanup = time.time()
    
    def should_respond(self, user_id: int, force_respond: bool = False) -> tuple[bool, float]:
        """Check if bot should respond and return (should_respond, chance)"""
        now = time.time()
        
        # Periodic cleanup
        if now - self.last_cleanup > self.config.CLEANUP_INTERVAL:
            self.cleanup_old_data()
        
        # Increment message count
        self.user_message_counts[user_id] += 1
        
        # Calculate scaled chance
        scaled_chance = self.config.BASE_CHANCE + self.user_message_counts[user_id] * self.config.SCALE_FACTOR
        chance = min(scaled_chance, self.config.MAX_CHANCE)  # Use configurable cap
        
        # If bot was mentioned, bypass all cooldowns and probability checks
        if force_respond:
            self.last_reply = now
            self.user_last_reply[user_id] = now
            self.user_message_counts[user_id] = 0  # Reset count after response
            return True, 1.0  # Return 100% chance to indicate it was a mention
        
        # Normal probability-based logic
        # Check global cooldown
        if now - self.last_reply < self.config.COOLDOWN:
            return False, chance
        
        # Check per-user cooldown
        if now - self.user_last_reply[user_id] < self.config.USER_COOLDOWN:
            return False, chance
        
        # Roll the dice
        if random.random() < chance:
            self.last_reply = now
            self.user_last_reply[user_id] = now
            self.user_message_counts[user_id] = 0  # Reset count after response
            return True, chance
        
        return False, chance
    
    def cleanup_old_data(self):
        """Clean up old user data to prevent memory bloat"""
        current_time = time.time()
        cutoff_time = current_time - (24 * 3600)  # Remove data older than 24 hours
        
        # Clean up old user reply times
        old_users = [user_id for user_id, last_time in self.user_last_reply.items() 
                     if last_time < cutoff_time]
        
        for user_id in old_users:
            if user_id in self.user_last_reply:
                del self.user_last_reply[user_id]
            if user_id in self.user_message_counts:
                del self.user_message_counts[user_id]
        
        if old_users:
            logger.info(f"Cleaned up data for {len(old_users)} inactive users")
        
        self.last_cleanup = current_time