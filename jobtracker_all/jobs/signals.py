from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import JobApplication

@receiver(pre_save, sender=JobApplication)
def notify_status_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old = JobApplication.objects.get(pk=instance.pk)
    except JobApplication.DoesNotExist:
        return
    if old.status != instance.status:
        user_email = instance.user.email
        send_mail(
            subject='Your job status has been updated.',
            message=f'The status of your job "{instance.title}" has changed from "{old.status}" to "{instance.status}"',
            from_email='no-reply@jobtracker.com',
            recipient_list=[user_email],
            fail_silently=False,
        )