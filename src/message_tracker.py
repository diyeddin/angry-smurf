import time
import random
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class MessageTracker:
    """
    The Social Battery Engine.
    Simulates a bot with a 'Tension Meter' that fills up based on chat activity,
    mood, and personal grudges (Beef).
    """
    
    def __init__(self, config):
        self.config = config
        
        # State Variables
        self.tension_meter = 0.0
        self.tension_threshold = 100.0  # Triggers when meter hits this
        
        # Tracking Data
        self.beef_ledger = defaultdict(int)  # {user_id: beef_level}
        self.last_beef_decay = time.time()
        
        # Mood System
        self.moods = {
            "Zen": 0.5,      # Hard to trigger
            "Normal": 1.0,   # Standard
            "Cranky": 2.0,   # Easy to trigger
            "Unhinged": 4.0  # Chaos mode
        }
        self.current_mood = "Normal"
        self.last_mood_switch = time.time()
        
        # Burst Mode (The Argument System)
        self.burst_active = False
        self.burst_target_id = None
        self.burst_end_time = 0

    def _update_mood(self):
        """Rotates the bot's mood periodically"""
        if time.time() - self.last_mood_switch > self.config.MOOD_SWITCH_INTERVAL:
            self.current_mood = random.choice(list(self.moods.keys()))
            self.last_mood_switch = time.time()
            logger.info(f"🔄 Mood shifted to: {self.current_mood}")

    def _update_beef_decay(self):
        """Reduces beef scores over time so the bot forgives eventually"""
        if time.time() - self.last_beef_decay > self.config.BEEF_DECAY_INTERVAL:
            for user in list(self.beef_ledger.keys()):
                if self.beef_ledger[user] > 0:
                    self.beef_ledger[user] -= 1
            self.last_beef_decay = time.time()

    def process_message(self, user_id: int, message_content: str, is_mention: bool) -> dict:
        """
        Analyzes message and determines if bot should trigger.
        Returns dict: {'trigger': bool, 'is_burst': bool}
        """
        self._update_mood()
        self._update_beef_decay()
        
        # 1. CHECK BURST MODE (Argument Priority)
        if self.burst_active:
            # If the target replies while we are angry, reply back instantly
            if user_id == self.burst_target_id:
                self.burst_active = False # End burst (or flip coin to continue)
                return {'trigger': True, 'is_burst': True}
            
            # If time ran out on burst mode
            if time.time() > self.burst_end_time:
                self.burst_active = False
                self.burst_target_id = None

        # 2. IMMEDIATE MENTION TRIGGER
        if is_mention:
            self._trigger_event(user_id)
            return {'trigger': True, 'is_burst': False}

        # 3. CALCULATE TENSION IMPACT
        base_impact = random.randint(5, 10)
        
        # Contextual Bonuses
        context_bonus = 0
        if len(message_content) > 200: context_bonus += 15   # Long rants annoy bot
        if message_content.isupper(): context_bonus += 20    # Caps lock annoys bot
        if "???" in message_content: context_bonus += 10     # Confusion annoys bot
        
        # Beef Multiplier (Do we hate this user?)
        user_beef_level = self.beef_ledger.get(user_id, 0)
        beef_mult = 1.0 + (user_beef_level * 0.25) # +25% tension per beef level
        
        # Mood Multiplier
        mood_mult = self.moods[self.current_mood]
        
        # Final Tension Math
        total_impact = (base_impact + context_bonus) * beef_mult * mood_mult
        self.tension_meter += total_impact
        
        # Log status occasionally
        if random.random() < 0.1:
            logger.info(f"🔋 Tension: {self.tension_meter:.1f}/{self.tension_threshold} | Mood: {self.current_mood}")

        # 4. CHECK THRESHOLD
        if self.tension_meter >= self.tension_threshold:
            self._trigger_event(user_id)
            return {'trigger': True, 'is_burst': False}
            
        return {'trigger': False, 'is_burst': False}

    def _trigger_event(self, user_id):
        """Resets tension and sets up next trigger state"""
        # Reset Meter
        self.tension_meter = 0
        # Randomize next threshold (80-150) so it's unpredictable
        self.tension_threshold = random.randint(80, 150)
        
        # Add Beef to the victim
        self.beef_ledger[user_id] += 1
        logger.info(f"🔥 TRIGGERED against user {user_id}. Their Beef level is now {self.beef_ledger[user_id]}")
        
        # Chance to enter Burst Mode (Argument Mode)
        # If we are Crank/Unhinged, higher chance to argue
        burst_chance = 0.3
        if self.current_mood in ["Cranky", "Unhinged"]:
            burst_chance = 0.6
            
        if random.random() < burst_chance:
            self.burst_active = True
            self.burst_target_id = user_id
            self.burst_end_time = time.time() + 60 # Lasts 60 seconds
            logger.info("💢 Entered BURST MODE (Argument expected)")