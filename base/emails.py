# from email import message
# from django.conf import settings
# from django.core.mail import send_mail


# def send_account_activation_email(email,email_token):
#     subject = "VERIFY Account created"
#     email_from = settings.EMAIL_HOST_USER
#     message = f'Hi, we are so pleased to have you registered on our platform.\nPlease Click on the link to verify your email. http://127.0.0.1:8000/accounts/activate/{email}'

#     send_mail(subject,message,email_from,[email])