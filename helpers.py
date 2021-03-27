import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
def mail(email_address, subject, message):
    me = "jaxton@boyuan12.me"
    password = "jaxton123@"
    
    msg = MIMEMultipart("alternative")
    msg['From'] = "Classcord-community@boyuan12.me"
    msg['To'] = email_address
    msg['Subject'] = subject

    html = message
    part2 = MIMEText(html, 'html')

    msg.attach(part2)


    s = smtplib.SMTP_SSL("mail.privateemail.com")

    s.login(me, password)

    s.sendmail(me, email_address, msg.as_string())
    s.quit()


mail("jaxton@boyuan12.me", "testing!", "<h1>Testing!</h1>")