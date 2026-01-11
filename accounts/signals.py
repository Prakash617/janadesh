from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
# from .utils import send_registration_email, send_membership_status_email
from accounts.models import User
from mail.helpers import EmailHelper


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """Send welcome email after user registration"""
    if created:
        try:
            mail = EmailHelper()
            subject = 'Welcome to Our Platform - Registration Successful'
    #         html_message = render_to_string('mails/registration_success.html', {
    #     'user': user,
    #     'full_name': user.get_full_name_nepali() or user.get_full_name(),
    # })
    #         plain_message = strip_tags(html_message)
            context ={
                'user': instance,
                'full_name': instance.full_name,
            }
    
            mail.send_template_email(subject=subject, template_name='mails/registration_success.html', context=context, recipient_list=[instance.email])
        except Exception as e:
            print(f"Failed to send registration email: {e}")