import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import time

sender_email = "info@essentecla.com"
# receiver_email = "receiver_mail@gmail.com"
password = "EvaLucia-2019"

message = MIMEMultipart("alternative")
message["Subject"] = "Necesitas una pagina web? Te podemos ayudar!"
message["From"] = sender_email

context = ssl.create_default_context()
server = smtplib.SMTP_SSL("smtp.hostinger.com.ar", 465, context=context)
server.ehlo()
server.login(sender_email, password)

with open('mail.html', 'r', encoding="utf8") as file:
    data = file.read().replace('\n', '')
count = 0

with open("date_{{TIME}}.csv") as file:
    reader = csv.reader(file)
    next(reader)
    for name, email, link in reader:
        # Create the plain-text and HTML version of your message
        html = data.format(name=name, link=link)

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(MIMEText(html, "html"))

        server.sendmail(
            sender_email, email, message.as_string()
        )

        count += 1
        print(str(count) + ". Sent to " + email)

        if(count%80 == 0):
            server.quit()
            print("Server cooldown for 100 seconds")
            time.sleep(100)
            server.ehlo()
            server.login(sender_email, password)

server.quit()
