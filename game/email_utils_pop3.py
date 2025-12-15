# email_utils_pop3.py
import poplib
from email import parser

def fetch_inbox_emails_pop3(pop3_user, pop3_pass):
    pop3_server = "127.0.0.1"
    emails = []

    # الاتصال بالسيرفر
    mail = poplib.POP3(pop3_server)
    mail.user(pop3_user)
    mail.pass_(pop3_pass)

    num_messages = len(mail.list()[1])

    # جلب كل رسالة
    for i in range(num_messages):
        raw_email = b"\n".join(mail.retr(i+1)[1])
        parsed_email = parser.Parser().parsestr(raw_email.decode('utf-8', errors='ignore'))

        body = ""
        if parsed_email.is_multipart():
            for part in parsed_email.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors='ignore')
        else:
            body = parsed_email.get_payload(decode=True).decode(errors='ignore')

        emails.append({
            "from": parsed_email["From"],
            "subject": parsed_email["Subject"],
            "body": body
        })
    print(emails)
    mail.quit()
    return emails
