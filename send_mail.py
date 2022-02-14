from dotenv import load_dotenv
import email, os, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from email.mime.application import MIMEApplication

load_dotenv()

port = 587  # For Start TLS

SMTP_URL = os.getenv("SMTP_URL")
SENDER_EMAIL =  os.getenv("SENDER_EMAIL")
RECEIVER_EMAIL =  os.getenv("RECEIVER_EMAIL")
PASSWORD =  os.getenv("PASSWORD")

# Create a secure SSL context
context = ssl.create_default_context()

def send_email(subject, body):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = SENDER_EMAIL
    message["To"] = RECEIVER_EMAIL
    message["Subject"] = subject
    message["Bcc"] = RECEIVER_EMAIL  # Recommended for mass emails
    
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    
    # filename = "document.pdf"  # In same directory as script

    for filename in os.listdir("attachments"):
        with open(f"attachments/{filename}", "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(filename)
                )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(filename)
        message.attach(part)
        os.remove(f"attachments/{filename}")
        
    text = message.as_string()
    with smtplib.SMTP(SMTP_URL, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text.encode('utf-8'))
    
send_email("Test subject", "Test body")
    
