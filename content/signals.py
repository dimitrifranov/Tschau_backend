from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from content.models import Post, PostLike, Notification

import os
import requests
import json


@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    if created:
        signal_id = instance.creator.profile.signal_id
        app_id = "56c16a44-f980-41c2-8a74-b4591cc6ab35"
        header = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "app_id": app_id,
            "include_player_ids": [signal_id],
            "contents": {"en": "nice Post"},
        }
        r = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=header,
            data=json.dumps(payload),
        )
        # print(r.text)


@receiver(post_save, sender=PostLike)
def create_post_like(sender, instance, created, **kwargs):
    if created:
        # print(instance)
        signal_id = instance.post.creator.profile.signal_id
        app_id = "56c16a44-f980-41c2-8a74-b4591cc6ab35"
        header = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "app_id": app_id,
            "include_player_ids": [signal_id],
            "contents": {"en": "hesche like becho vom " + instance.liker.username},
        }
        r = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=header,
            data=json.dumps(payload),
        )
        user = User.objects.get(pk=instance.post.creator.pk)
        notif = Notification.objects.create(
            content="hesche like becho vom " + instance.liker.username, user=user,
        )
        # print(r.text)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     # user = instance
#     # if created:
#     #     profile = UserProfile(user=user)
#     #     profile.save()
#     instance.profile.save()
