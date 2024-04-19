import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# взаимодействие с почтой
def send_mail(email, title, text):
    try:
        addr_form = os.getenv("FROM")
        password = os.getenv("PASSWORD")

        msg = MIMEMultipart()
        msg['From'] = addr_form
        msg['To'] = email
        msg['Subject'] = title

        body = text
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP_SSL(os.getenv("HOST"), int(os.getenv("PORT")))
        server.login(addr_form, password)

        server.send_message(msg)
        server.quit()
        return True
    except:
        return False
