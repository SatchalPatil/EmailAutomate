import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ollama

def generate_email_content(prompt):
    structured_prompt = (
        "You are an AI email assistant. Your task is to generate a well-structured and professional email based on the user's input.\n\n"
        "Instructions:\n"
        "1. Understand the Context: Carefully analyze the user's input to determine the purpose of the email. Identify the subject, tone, and key details.\n"
        "2. Ensure Proper Formatting:\n"
        "   - Always structure the email as follows:\n"
        "     Subject: <email subject>\n"
        "     Body:\n"
        "     <email body>\n"
        "   - The subject should be clear, concise, and relevant (under 10 words).\n"
        "   - The body should be well-structured, maintaining logical flow.\n"
        "3. Adjust the Tone Based on Intent:\n"
        "   - If the email is formal (e.g., to a professor, boss, or client), use professional language.\n"
        "   - If it’s casual (e.g., to a friend or colleague), use a friendly and warm tone.\n"
        "4. Avoid Unnecessary Filler:\n"
        "   - Keep the email concise yet informative.\n"
        "   - Ensure the key message is clearly conveyed within a few sentences.\n"
        "5. Grammar and Clarity: Ensure the email is grammatically correct, free of spelling mistakes, and easy to read.\n"
        "6. Personalization and Call to Action (Optional):\n"
        "   - If the user mentions a name, personalize the greeting (e.g., Dear John,).\n"
        "   - If relevant, include a polite closing statement or call to action.\n\n"
        "User Input:\n"
        f"{prompt}\n\n"
        "Expected Output Format:\n"
        "Subject: <email subject>\n"
        "Body:\n" 
        "<email body>"
    )
    response = ollama.chat(model='qwen2.5:3B', messages=[{"role": "user", "content": structured_prompt}])
    email_content = response['message']['content']

    if "Subject:" in email_content and "Body:" in email_content:
        subject = email_content.split("Subject:", 1)[1].split("Body:", 1)[0].strip()
        body = email_content.split("Body:", 1)[1].strip()
        return subject, body
    else:
        return "No Subject", email_content

def send_email(to_email, subject, body):
    EMAIL_ADDRESS = "autoemail22@gmail.com"
    APP_PASSWORD = "wufr haao cpmg ksaw"

    msg = MIMEMultipart()
    msg["From"] = "Happy Patil <autoemail22@gmail.com>"
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, APP_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())

def main():
    prompt = input("Describe the email you want to send: ")
    subject, body = generate_email_content(prompt)
    
    to_email = input("Enter recipient email: ")
    
    print("\nGenerated Email:")
    print(f"Subject: {subject}")
    print(f"Body:\n{body}\n")

    send_email(to_email, subject, body)
    print("✅ Email sent successfully!")

if __name__ == "__main__":
    main()
