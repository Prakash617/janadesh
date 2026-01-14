from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import StaffRole


@receiver(post_save, sender=StaffRole)
def apply_role_permissions(sender, instance, **kwargs):
    user = instance.user
    role = instance.role

    # Clear existing permissions
    user.user_permissions.clear()

    # Assign role permissions
    user.user_permissions.add(*role.permissions.all())
