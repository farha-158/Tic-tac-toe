import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_real_email( subject, body):
    # بيانات حسابك الحقيقي
    smtp_server = "smtp.gmail.com"  # لو Gmail
    smtp_port = 587
    from_email = "developerbackend65@gmail.com"
    password = "ixqwlfaxfvxdidzj"  
    # إعداد الرسالة
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = os.getenv("REAL_EMAIL")
    msg['Subject'] = subject
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
        <h2 style="color: #4CAF50;">Hello!</h2>
        <p>{body}</p>
        <hr>
        <p style="font-size: 0.9em; color: #555;">
        This is a test email sent from Python.<br>
        Have a nice day! 😊
        </p>
    </body>
    </html>
    """
    part = MIMEText(html_content, "html")
    msg.attach(part)

    # الاتصال بالخادم وإرسال الرسالة
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, password)
    server.send_message(msg)
    server.quit()

    print(f"Email sent to successfully!")
