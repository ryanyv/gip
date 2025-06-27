from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

from .models import Photo, Property

@receiver(post_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    if instance.image and hasattr(instance.image, 'path') and os.path.isfile(instance.image.path):
        try:
            os.remove(instance.image.path)
        except OSError:
            pass

@receiver(post_delete, sender=Property)
def delete_property_video(sender, instance, **kwargs):
    if instance.video and hasattr(instance.video, 'path') and os.path.isfile(instance.video.path):
        try:
            os.remove(instance.video.path)
        except OSError:
            pass
