from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class EmailHelper:
    """Helper class for sending emails with templates and attachments"""
    
    @staticmethod
    def send_simple_email(subject, message, recipient_list, from_email=None):
        """
        Send a simple text email
        
        Args:
            subject (str): Email subject
            message (str): Email body
            recipient_list (list): List of recipient email addresses
            from_email (str, optional): Sender email. Defaults to settings.DEFAULT_FROM_EMAIL
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            send_mail(
                subject=subject,
                message=message,
                from_email=from_email,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            logger.info(f"Simple email sent to {recipient_list}: {subject}")
            return True
        except Exception as e:
            logger.error(f"Failed to send simple email: {str(e)}")
            return False
    
    @staticmethod
    def send_template_email(subject, template_name, context, recipient_list, 
                          from_email=None, attachments=None):
        """
        Send an HTML email using a Django template
        
        Args:
            subject (str): Email subject
            template_name (str): Path to HTML template
            context (dict): Context data for template rendering
            recipient_list (list): List of recipient email addresses
            from_email (str, optional): Sender email
            attachments (list, optional): List of tuples (filename, content, mimetype)
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            
            # Render HTML content
            html_content = render_to_string(template_name, context)
            
            # Create plain text version
            text_content = strip_tags(html_content)
            
            # Create email message
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=recipient_list
            )
            
            # Attach HTML version
            email.attach_alternative(html_content, "text/html")
            
            # Add attachments if provided
            if attachments:
                for filename, content, mimetype in attachments:
                    email.attach(filename, content, mimetype)
            
            email.send(fail_silently=False)
            logger.info(f"Template email sent to {recipient_list}: {subject}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send template email: {str(e)}")
            return False
    
    @staticmethod
    def send_welcome_email(user_email, user_name, context=None):
        """
        Send a welcome email to new users
        
        Args:
            user_email (str): User's email address
            user_name (str): User's name
            context (dict, optional): Additional context data
            
        Returns:
            bool: True if email was sent successfully
        """
        default_context = {
            'user_name': user_name,
            'site_name': getattr(settings, 'SITE_NAME', 'Our Site'),
            'site_url': getattr(settings, 'SITE_URL', ''),
        }
        
        if context:
            default_context.update(context)
        
        return EmailHelper.send_template_email(
            subject=f"Welcome to {default_context['site_name']}!",
            template_name='emails/welcome_email.html',
            context=default_context,
            recipient_list=[user_email]
        )
    
    @staticmethod
    def send_password_reset_email(user_email, reset_link, user_name=None):
        """
        Send a password reset email
        
        Args:
            user_email (str): User's email address
            reset_link (str): Password reset URL
            user_name (str, optional): User's name
            
        Returns:
            bool: True if email was sent successfully
        """
        context = {
            'user_name': user_name or 'User',
            'reset_link': reset_link,
            'site_name': getattr(settings, 'SITE_NAME', 'Our Site'),
        }
        
        return EmailHelper.send_template_email(
            subject='Password Reset Request',
            template_name='emails/password_reset_email.html',
            context=context,
            recipient_list=[user_email]
        )
    
    @staticmethod
    def send_notification_email(user_email, notification_type, context):
        """
        Send a notification email
        
        Args:
            user_email (str): User's email address
            notification_type (str): Type of notification
            context (dict): Context data for the notification
            
        Returns:
            bool: True if email was sent successfully
        """
        subject_map = {
            'comment': 'New Comment on Your Post',
            'like': 'Someone Liked Your Post',
            'follow': 'You Have a New Follower',
            'mention': 'You Were Mentioned',
        }
        
        subject = subject_map.get(notification_type, 'New Notification')
        
        return EmailHelper.send_template_email(
            subject=subject,
            template_name=f'emails/notification_{notification_type}.html',
            context=context,
            recipient_list=[user_email]
        )
    
    @staticmethod
    def send_bulk_email(subject, message, recipient_list, from_email=None, 
                    batch_size=100):
        """
        Send bulk emails in batches
        
        Args:
            subject (str): Email subject
            message (str): Email body
            recipient_list (list): List of recipient email addresses
            from_email (str, optional): Sender email
            batch_size (int): Number of emails to send per batch
            
        Returns:
            dict: Statistics about sent emails
        """
        from_email = from_email or settings.DEFAULT_FROM_EMAIL
        total = len(recipient_list)
        sent = 0
        failed = 0
        
        # Send in batches
        for i in range(0, total, batch_size):
            batch = recipient_list[i:i + batch_size]
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=from_email,
                    recipient_list=batch,
                    fail_silently=False,
                )
                sent += len(batch)
                logger.info(f"Batch email sent to {len(batch)} recipients")
            except Exception as e:
                failed += len(batch)
                logger.error(f"Failed to send batch email: {str(e)}")
        
        return {
            'total': total,
            'sent': sent,
            'failed': failed,
            'success_rate': (sent / total * 100) if total > 0 else 0
        }
    
    @staticmethod
    def send_contact_form_email(name, email, subject, message, admin_email=None):
        """
        Send an email from a contact form
        
        Args:
            name (str): Sender's name
            email (str): Sender's email
            subject (str): Email subject
            message (str): Email message
            admin_email (str, optional): Admin email to receive the message
            
        Returns:
            bool: True if email was sent successfully
        """
        admin_email = admin_email or getattr(settings, 'ADMIN_EMAIL', 
                                            settings.DEFAULT_FROM_EMAIL)
        
        context = {
            'sender_name': name,
            'sender_email': email,
            'message': message,
        }
        
        return EmailHelper.send_template_email(
            subject=f"Contact Form: {subject}",
            template_name='emails/contact_form.html',
            context=context,
            recipient_list=[admin_email]
        )
    
    @staticmethod
    def send_email_verification(user_email, verification_link, user_name=None):
        """
        Send an email verification link
        
        Args:
            user_email (str): User's email address
            verification_link (str): Email verification URL
            user_name (str, optional): User's name
            
        Returns:
            bool: True if email was sent successfully
        """
        context = {
            'user_name': user_name or 'User',
            'verification_link': verification_link,
            'site_name': getattr(settings, 'SITE_NAME', 'Our Site'),
        }
        
        return EmailHelper.send_template_email(
            subject='Verify Your Email Address',
            template_name='emails/email_verification.html',
            context=context,
            recipient_list=[user_email]
        )