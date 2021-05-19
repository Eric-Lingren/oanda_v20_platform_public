import logging
import smtplib
from io import StringIO
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_notification(from_email, server_password, recipient, subject, message):

    # BUILD THE EMAIL 
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = recipient
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    # SENDS THE EMAIL VIA SECURE SMTP
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(from_email, server_password)
    server.sendmail(from_email, recipient, text)

    # GRACEFUL EXIT
    server.close()
    return True