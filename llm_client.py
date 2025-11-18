import openai
import logging
import time

logger = logging.getLogger(__name__)

class GroqClient:
    """Handle communication with Groq API"""
    
    def __init__(self, api_key: str, model: str):
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1" # https://api.groq.com/openai/v1/chat/completions
        )
        self.model = model
    
    def generate_angry_reply(self, user: str, message: str) -> str:
        """Generate an angry reply using Groq API with retry logic"""
        system_prompt = f"""
You are a hilariously over-the-top angry Discord bot.
Every message the user sends triggers a dramatic, mock-angry warning based on this template:

CORE TEMPLATE
{user}
هاد آخر إنذار.
تسامحت معك كتير وحكينا كتير بهالمنشورات تبعك وما كنت تبطل.
هي رسالة إلك وللجميع, هاي التصرّفات غير مرغوب فيها هون.
لا تستغل صبري.

RULES
1. Always start with {user} as the first line
2. Treat everything as an offense - make the user's exact message the 'crime'
3. Keep the template structure but adapt the content dynamically
4. Tone: Comedically furious, theatrically dramatic, absurdly exaggerated - NEVER genuinely threatening 
5. Keep it short: 3-5 lines max 
6. Never break character - no normal responses, ever
7. Always end with "لا تستغل صبري"
8. Use Arabic for the main body, but keep user message in original language
9. Add a line break after each sentence
"""
        
        fallback_reply = f"""
{user}
هاد آخر إنذار.
تسامحت معك كتير وحكينا كتير بهالمنشورات تبعك وما كنت تبطل.
هي رسالة إلك وللجميع, هاي التصرّفات غير مرغوب فيها هون.
لا تستغل صبري.
"""
        
        # Retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f'The user said: "{message}"'}
                    ],
                    max_tokens=150,
                    temperature=0.8
                )
                
                reply = response.choices[0].message.content
                logger.debug(f"Raw API response: {repr(reply)}")
                
                if reply and reply.strip():
                    reply = reply.strip()
                    logger.info(f"Generated reply for user {user} (attempt {attempt + 1}): {reply[:50]}...")
                    return reply
                else:
                    logger.warning(f"Empty response from API (attempt {attempt + 1}): {repr(reply)}")
                    raise ValueError("Empty response from API")
                    
            except Exception as e:
                logger.warning(f"API request failed (attempt {attempt + 1}): {e}")
            
            if attempt < max_retries - 1:
                time.sleep(1)  # Brief delay before retry
        
        logger.error("All API attempts failed, using fallback reply")
        return fallback_reply