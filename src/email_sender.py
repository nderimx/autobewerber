import smtplib
from getpass import getpass
import os

from email.message import EmailMessage

def send_application(sender, receiver, subject, message, attachments, password=""):
    msg = EmailMessage()
    msg.set_content(message)

    for attachment in attachments:
        with open(attachment, 'rb') as certs_file:
            certs_raw = certs_file.read()
            msg.add_attachment(certs_raw, maintype='application',
            subtype="pdf", disposition="attachment", filename=os.path.basename(attachment))

    msg['Subject']  = subject
    msg['To']       = receiver
    msg['From']     = sender

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587) # or 465
        smtpObj.ehlo()
        smtpObj.starttls()
        if password == "":
            password = getpass()
        smtpObj.login(msg['From'], password)
        smtpObj.send_message(msg)
        smtpObj.quit()     
        print("Successfully sent email")
    except Exception as e:
        print("Error: unable to send email: %s" % e)