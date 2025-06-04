# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
# from django.conf import settings
# from .models import User

# @receiver(post_save, sender=User)
# def send_verification_email(sender, instance, created, **kwargs):
#     if created and not instance.is_active:
#         send_mail(
#             'Verify Your Email',
#             'Please verify your email to activate your account. Click here: [Verification Link]',
#             settings.DEFAULT_FROM_EMAIL,
#             [instance.email],
#             fail_silently=False,
#         )