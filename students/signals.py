from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Ball


@receiver(post_save, sender=Ball)
def ball_changed(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "dashboard",
        {
            "type": "ball_update",   # consumerdagi metod nomi
            "student_id": instance.student_id,
            "ball": instance.coin,
        },
    )