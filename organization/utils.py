from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_registration_email(user):
    """Send welcome email after successful registration"""
    subject = 'Welcome to Our Platform - Registration Successful'
    html_message = render_to_string('mails/registration_success.html', {
        'user': user,
        'full_name': user.get_full_name_nepali() or user.get_full_name(),
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_membership_status_email(membership, status):
    """Send email notification when membership status changes"""
    if status == 'approved':
        subject = 'Membership Application Approved'
        template = 'mails/membership_approved.html'
    elif status == 'rejected':
        subject = 'Membership Application Update'
        template = 'mails/membership_rejected.html'
    else:
        return
    
    html_message = render_to_string(template, {
        'membership': membership,
        'full_name': membership.get_full_name(),
    })
    plain_message = strip_tags(html_message)
    
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [membership.email],
        html_message=html_message,
        fail_silently=False,
    )