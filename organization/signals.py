from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import  MembershipRegistration
from .utils import send_registration_email, send_membership_status_email


# @receiver(post_save, sender=CustomUser)
# def user_post_save(sender, instance, created, **kwargs):
#     """Send welcome email after user registration"""
#     if created:
#         try:
#             send_registration_email(instance)
#         except Exception as e:
#             print(f"Failed to send registration email: {e}")


@receiver(pre_save, sender=MembershipRegistration)
def membership_status_changed(sender, instance, **kwargs):
    """Track status changes and send notification emails"""
    if instance.pk:
        try:
            old_instance = MembershipRegistration.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                if instance.status in ['approved', 'rejected']:
                    send_membership_status_email(instance, instance.status)
        except MembershipRegistration.DoesNotExist:
            pass

