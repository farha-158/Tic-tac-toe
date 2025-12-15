import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv


load_dotenv()
def send_local_email(emailTo,subject, body):
    msg = EmailMessage()
    msg["From"] = os.getenv('EMAIL_LOCALHOST')  # حسابك على السيرفر المحلي
    msg["To"] = emailTo
    msg["Subject"] = subject
    msg.set_content(body)

    # الاتصال بـ hMailServer المحلي
    with smtplib.SMTP("127.0.0.1", 25) as smtp:
        smtp.send_message(msg)

    print(f"Local email sent to!")
