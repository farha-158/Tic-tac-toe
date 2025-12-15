# email_utils.py
import imaplib
import email

def fetch_inbox_emails(imap_user, imap_pass):
    imap_server = "127.0.0.1"
    mail = imaplib.IMAP4(imap_server)
    mail.login(imap_user, imap_pass)
    mail.select("INBOX")

    emails = []

    status, messages = mail.search(None, "ALL")
    for num in messages[0].split():
        status, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        emails.append({
            "from": msg["From"],
            "subject": msg["Subject"],
            "body": body
        })

    mail.logout()
    return emails
