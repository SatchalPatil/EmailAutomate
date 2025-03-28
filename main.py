import logging
from email_workflow import Auto_emailing
from intent_detection import detect_email_intent
from chat_processing import process_general_chat

# Configure logging for the whole application
logging.basicConfig(
    level=logging.WARNING,  # Only warnings and errors will be printed to the console
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chatbot.log"),  # Optionally log detailed info to a file
        logging.StreamHandler()               # Console output
    ]
)

def general_chatbot():
    """
    General-purpose chatbot that routes email requests to Auto_emailing() if detected via LLM intent analysis.
    """
    print("Welcome to the General-Purpose Chatbot! (Type 'exit' to quit)")
    while True:
        user_input = input("User: ")
        if user_input.strip().lower() == "exit":
            print("Goodbye!")
            break
        
        # Use the LLM-based intent detection to decide if the query is an email intent.
        if detect_email_intent(user_input):
            print("It looks like you want to send an email. Let's proceed with the email automation workflow.")
            Auto_emailing()
        else:
            # Otherwise, process the conversation normally.
            response = process_general_chat(user_input)
            print(f"LLM: {response}")

def main():
    general_chatbot()

if __name__ == "__main__":
    main()
