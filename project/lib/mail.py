import smtplib
from django.conf import settings

def send(to, subject, text):
    if not settings.EMAIL_SERVER:
        return
    
    if not isinstance(to, (list, tuple)):
        to = [to]
    
    message = "From: %s\r\n" \
        "To: %s\r\n" \
        "Subject: %s\r\n" \
        "\r\n" \
        "%s" % (settings.EMAIL_FROM, ", ".join(to), subject, text)
        
    server = smtplib.SMTP_SSL(settings.EMAIL_SERVER)
    if settings.EMAIL_FROM_PASSWORD:
        server.login(settings.EMAIL_FROM, settings.EMAIL_FROM_PASSWORD)
    server.sendmail(settings.EMAIL_FROM, to, message)
    server.quit()