import smtplib, ssl
import random
from email.mime.text import MIMEText
from email.header import Header
from email.generator import Generator
from io import StringIO
import json
import datetime
import sys

average_fika_cravers = None
fika_range_lower = None
fika_range_upper = None
day = None

with open('Settings.json') as f:
    data = json.load(f)
    day = int(data["day"])
    average_fika_cravers = int(data["average deltagare"])
    fika_range_lower = int(data["max deltagar subtraktion"])
    fika_range_upper = int(data["max deltagar addition"])
    

dayToday = datetime.datetime.today().weekday()
date = datetime.datetime.today().date()

lastWrittenDate = ""
with open("LastWritten.txt", "r") as f:
    lastWrittenDate = f.read()
    
if dayToday != 3 or str(date) == lastWrittenDate:
    sys.exit()

with open("LastWritten.txt", "w") as f:
    f.write(str(date))




port = 587  # For starttls
smtp_server = "smtp.gmail.com"
sender_email = ""
password = ""
receiver_email = ""

with open('Credentials.json') as f:
    data = json.load(f)
    sender_email = data["sender"]
    password = data["password"]
    receiver_email = data["recipient"]

print(sender_email)
print(password)
print(receiver_email)

start = ["Hallå", "Hej", 'Tjenare', 'Halloj', 'Jenixen', 'Tjabba', 'Morsning', 'Tjabba tjena hallå', "Tjo", 'Morsning korsning', 'Hejsan svejsan', 'Tjohej']
intro = ["Då var det dags för spelonsdags klubben igen och våra medlemmar vill ha fika",
         "Imorgon är det spelonsdags klubb och vi hade högst uppskattat fika",
         "Vi hade uppskattat fika till spelonsdags klubben imorgon"]



message = """
{}, Nasir.
{}.
Vi uppskattar att ca {} personer kommer komma.
Mvh, Joshua Jeffmar 1C""".format(random.choice(start), random.choice(intro),
                                 average_fika_cravers + random.randint(-fika_range_lower, fika_range_upper))
print(message)

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    msg = MIMEText(message, _charset="UTF-8")
    msg['Subject'] = Header("Fika spel-onsdags klubben", "utf-8")
    str_io = StringIO()
    g = Generator(str_io, False)
    g.flatten(msg)
    
    server.sendmail(sender_email, receiver_email, str_io.getvalue())
