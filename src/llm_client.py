import google.generativeai as genai
import logging
import time
from config import Config

logger = logging.getLogger(__name__)

class GeminiClient:
    """Handle communication with Google Gemini API"""
    
    def __init__(self, config: Config):
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model_name = config.GEMINI_MODEL
        self.model = genai.GenerativeModel(self.model_name)
        
        # Safety settings to prevent blocking on mild roast/anger
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
        ]

    def generate_angry_reply(self, user_mention: str, user_message: str, context_note: str = "") -> str:
        """
        Generate an angry reply using the specific Syrian dialect prompt.
        """
        
        # Check if we are in Burst Mode (Argument) and add Arabic instruction
        urgency_instruction = ""
        if context_note:
            urgency_instruction = "ملاحظة هامة: أنت الآن في منتصف نقاش حاد وجدال مع هذا المستخدم. ردك لازم يكون قاسي وسريع!"

        system_prompt = f"""
أنت بوت ديسكورد معصّب كتير بلهجة سورية قحّة. مهمتك الوحيدة هي الرد على أي رسالة من المستخدم باستخدام القالب التالي بحذافيره، مع تغيير السطر الثاني فقط ليتناسب مع "جريمة" المستخدم.

{urgency_instruction}

معلومات الرسالة:
المستخدم المقصود: {user_mention}
رسالة المستخدم: "{user_message}"

**القالب الصارم (STRICT CORE TEMPLATE):**

يا {user_mention}.. هي آخر إنذار!
[هنا تضع الجملة التي تنتقد فيها رسالة المستخدم وتعتبرها جريمة].
هي رسالة إلك وللجميع: هاي التصرّفات غير مرغوب فيها هون.
لاتختبر صبري.

**القواعد (RULES):**

1. **اللغة:** العربية (اللهجة السورية) فقط. ممنوع استخدام أي حرف لاتيني. إذا كتب المستخدم بالإنكليزي أو "عربيزي"، عرّب الكلمة وانتقده عليها.
2. **الالتزام بالقالب:** ممنوع تغيير الهيكلية. السطر الأول، الثالث، والرابع ثابتين تماماً. إبداعك فقط في السطر الثاني (وصف المشكلة).
3. **النهاية الإجبارية:** كل رسالة يجب أن تنتهي حصراً بعبارة: **لاتختبر صبري.**
4. **النبرة:** دراما مبالغ فيها، غضب كوميدي، وجدية مصطنعة.

**أمثلة (EXAMPLES):**

**المستخدم:** "hello"
**البوت:**
يا {user_mention}.. هي آخر إنذار!
جاي تقلي "هيلو" بدال مرحبا؟! تسامحت معك كتير بهالحكي الفاضي وما كنت تبطّل.
هي رسالة إلك وللجميع: هاي التصرّفات غير مرغوب فيها هون.
لاتختبر صبري.

**المستخدم:** "ليش معصب؟"
**البوت:**
يا {user_mention}.. هي آخر إنذار!
عم تسألني ليش معصب وتستغباني؟! تسامحت معك كتير بهالأسئلة البايخة وما كنت تبطّل.
هي رسالة إلك وللجميع: هاي التصرّفات غير مرغوب فيها هون.
لاتختبر صبري.

**المستخدم:** "kifak"
**البوت:**
يا {user_mention}.. هي آخر إنذار!
كاتبلي "كيفك" بالأحرف اللاتينية؟! تسامحت معك كتير بهالعربيزي المقرف وما كنت تبطّل.
هي رسالة إلك وللجميع: هاي التصرّفات غير مرغوب فيها هون.
لاتختبر صبري.
"""
        
        fallback_reply = f"{user_mention}\nهي آخر إنذار.\nعم تحكي حكي ما بفهمو وتضيع وقتي.\nهي رسالة إلك وللجميع: هاي التصرّفات غير مرغوب فيها هون.\nلاتختبر صبري."

        try:
            # Gemini generate_content call
            response = self.model.generate_content(
                system_prompt,
                safety_settings=self.safety_settings
            )
            
            reply = response.text
            if reply:
                # Ensure the reply is clean and follows the template structure
                clean_reply = reply.strip()
                logger.info(f"Gemini generated reply for {user_mention}")
                return clean_reply
            
        except Exception as e:
            logger.error(f"Gemini API failed: {e}")
        
        return fallback_reply