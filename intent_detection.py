import logging
import ollama  

logger = logging.getLogger(__name__)

def detect_email_intent(user_input):
    """
    Uses an LLM model to detect if the user's input indicates an intent to send an email.
    Returns True if the intent is to send an email, otherwise False.
    """
    intent_prompt = (
        "You are an intent detection assistant. Analyze the following user input and determine whether the user intends to send an email. "
        "If the user's intent is to send an email (for example, the user might say 'I need to send a project update to my manager'), "
        "simply respond with the word 'email'. Otherwise, respond with 'normal'.\n\n"
        f"User Input: {user_input}\n\n"
        "Your response:"
    )
    try:
        response = ollama.chat(model='qwen2.5:3B', messages=[{"role": "user", "content": intent_prompt}])
        intent = response['message']['content'].strip().lower()
        logger.info(f"Intent detection result: {intent}")
        return intent == 'email'
    except Exception as e:
        logger.error(f"Error detecting email intent: {e}")
        #for error
        return False
