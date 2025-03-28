import sys
from email_workflow import generate_email_content, modify_email_content, send_email
from intent_detection import detect_email_intent
from chat_processing import process_general_chat

def main():
    mode = "chat"         # "chat" or "email"
    email_stage = None    # For email workflow: "init", "review", "modify", "confirm"
    generated_email = None

    print("Welcome to the FrobeAI Assistant (type 'exit' to quit)")
    
    while True:
        user_input = input("User: ").strip()
        if user_input.lower() == "exit":
            print("Goodbye!")
            sys.exit(0)
        
        if mode == "chat":
            # Instead of echoing the user's input, process it directly.
            if detect_email_intent(user_input):
                print("System: It looks like you want to send an email. Switching to email mode.")
                print("System: Please provide a description for the email you want to send:")
                mode = "email"
                email_stage = "init"
            else:
                response = process_general_chat(user_input)
                print(f"LLM: {response}")
        
        elif mode == "email":
            # Process email automation workflow in stages.
            if email_stage == "init":
                # The user's input is treated as the email description.
                generated_email = generate_email_content(user_input)  # Returns (subject, body, full_email)
                subject, body, full_email = generated_email
                print("\nSystem: Generated Email:")
                print(f"Subject: {subject}")
                print(f"Body: {body}\n")
                print("System: Reply with 'yes' to send, 'change' to modify, or 'cancel' to abort the email workflow.")
                email_stage = "review"
            elif email_stage == "review":
                if user_input.lower() == "yes":
                    print("System: Please provide the recipient's email address:")
                    email_stage = "confirm"
                elif user_input.lower() == "change":
                    print("System: Please provide your suggestions for modifications:")
                    email_stage = "modify"
                elif user_input.lower() == "cancel":
                    print("System: Email workflow cancelled. Returning to general chat.")
                    mode = "chat"
                    email_stage = None
                else:
                    print("System: Invalid response. Reply with 'yes', 'change', or 'cancel'.")
            elif email_stage == "modify":
                suggestions = user_input
                generated_email = modify_email_content(generated_email[2], suggestions)
                subject, body, full_email = generated_email
                print("\nSystem: Modified Email:")
                print(f"Subject: {subject}")
                print(f"Body: {body}\n")
                print("System: Reply with 'yes' to send, 'change' to modify further, or 'cancel' to abort the email workflow.")
                email_stage = "review"
            elif email_stage == "confirm":
                recipient = user_input
                try:
                    send_email(recipient, generated_email[0], generated_email[1])
                    print("System: ✅ Email sent successfully!")
                except Exception as e:
                    print("System: ❌ Failed to send email. Please check logs for details.")
                # Reset back to chat mode after sending the email.
                mode = "chat"
                email_stage = None

if __name__ == "__main__":
    main()
