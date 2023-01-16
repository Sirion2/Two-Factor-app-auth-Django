import uuid
from django.conf import settings
from django.core.mail import EmailMessage, send_mail

class Token:
    def token_gen(self):
        auth_token_gen = uuid.uuid4().hex[:6].upper()
        return auth_token_gen

    def send_mail(self, user_email, token):
        email = str(user_email)
        subject = "Token"
        message = "Hello your token is: " + token
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)