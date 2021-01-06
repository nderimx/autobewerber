from email_sender import send_application
message_file = "message_without_greeting.txt"

with open(message_file) as f:
    message = "Hallo" + f.read()

sender      = "xhemajlinderim@gmail.com"
receiver    = "nderimx@gmail.com"
subject     = "Test Subject"
attachments = ["Lebenslauf.pdf", "Zeugnisse_und_Diplome.pdf"]

send_application(sender, receiver, subject, message, attachments)