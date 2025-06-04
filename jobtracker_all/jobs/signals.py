from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import JobApplication
import logging
logger = logging.getLogger(__name__)

@receiver(pre_save, sender=JobApplication)
def notify_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = JobApplication.objects.get(pk=instance.pk)
    except JobApplication.DoesNotExist:
        logger.info('Old object not found. No notification sent.')
        return
    
    if old.status != instance.status:
        logger.info("Status change detected, sending email.")
        user_email = instance.user.email
        send_mail(
            subject='Your job status has been updated.',
            message=f'The status of your job "{instance.title}" has changed from "{old.status}" to "{instance.status}"',
            from_email='no-reply@jobtracker.com',
            recipient_list=[user_email],
            fail_silently=False,
        )

    if old.interview_date != instance.interview_date and instance.interview_date:
        logger.info("Interview date change detected, sending email.")
        user_email = instance.user.email
        send_mail(
            subject='You have an interview scheduled!',
            message=(
                f'You have an interview scheduled!\n'
                f'Your interview for the {instance.position} position you applied for at {instance.company}\n\n'
                f'is scheduled for: {instance.interview_date.strftime("%d/%m/%Y at %H:%M")}.'
            ),
            from_email='no-reply@jobtracker.com',
            recipient_list=[user_email],
            fail_silently=False,
        )