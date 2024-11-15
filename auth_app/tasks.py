from celery import shared_task
from django.core.mail import send_mail


@shared_task
def ConfirmationMail(first_name, last_name, userid,to_email):
    send_mail(
        "Registration Successfull!",
        
        f"""Dear {first_name} {last_name},

Welcome to OUR Website! We're excited to have you join our community.

To complete your registration and activate your account, please confirm your email address by clicking the link below:

{userid}

If you didn't register for an account, please ignore this email.

Thank you for choosing OUR Website! If you have any questions or need assistance, feel free to reply to this email or contact our support team.

Best regards,
Mr. Tirth Sharma
OUR Website Team
22bt04139@gsfcuniversity.ac.in """,

        "dummyforproject09@gmail.com",
        [to_email],
        fail_silently = False,
    )



@shared_task
def OTPMail(otp, first_name, last_name, to_email):
    send_mail(
        "Don't Share the OTP!",
        
        f"""Dear {first_name} {last_name},

We received a request to reset the password for your account. To proceed with resetting your password, please use the One-Time Password (OTP) provided below:

Your OTP: {otp}

This OTP is valid for the next 40 seconds. Please enter it on the password reset page to create a new password.

If you did not request a password reset, please ignore this email. Your account remains secure, and no changes have been made.

For any concerns or if you need further assistance, please contact our support team.

Best Regards,
OUR Website
22bt04139@gsfcuniversity.ac.in """,
        "dummyforproject09@gmail.com",
        [to_email],
        fail_silently = False,
    )