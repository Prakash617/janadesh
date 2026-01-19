from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Contact
from mail.helpers import EmailHelper   # adjust app path if needed


@receiver(post_save, sender=Contact)
def send_contact_received_email(sender, instance, created, **kwargs):
    """
    Send confirmation email to user when a contact message is created
    """
    if not created:
        return

    context = {
        "name": instance.name,
        "subject": instance.subject,
        "site_name": "Support Team",  # or settings.SITE_NAME
    }

    EmailHelper.send_template_email(
        subject="We have received your message",
        template_name="mails/contact_confirmation.html",
        context=context,
        recipient_list=[instance.email],
    )
