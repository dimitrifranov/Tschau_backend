from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from content.models import Post, PostLike, Notification, Comment

import os
import requests
import json


@receiver(post_save, sender=Post)
def create_post(sender, instance, created, **kwargs):
    if created:
        message = instance.creator.username + " hat einen neuen Beitrag geteilt."
        follower_ids = []
        for follower in instance.creator.follower.all():
            if (
                follower.user_from.profile.signal_id
                and follower.user_from.profile.follow_post_notifs
            ):
                follower_ids.append(follower.user_from.profile.signal_id)
            user = User.objects.get(pk=follower.user_from.pk)
            link = (
                "/groups/" + str(instance.group.id) + "/post/" + str(instance.id) + "/"
            )
            notif = Notification.objects.create(
                content=message, user=user, link=link, actor=instance.creator
            )

        if len(follower_ids):
            app_id = "56c16a44-f980-41c2-8a74-b4591cc6ab35"
            header = {"Content-Type": "application/json; charset=utf-8"}
            payload = {
                "app_id": app_id,
                "include_player_ids": follower_ids,
                "contents": {"en": message},
                "url": "https://social-tests.herokuapp.com" + link,
            }
            r = requests.post(
                "https://onesignal.com/api/v1/notifications",
                headers=header,
                data=json.dumps(payload),
            )

        # print(r.text)


@receiver(post_save, sender=PostLike)
def create_post_like(sender, instance, created, **kwargs):
    if created and instance.post.creator.profile.like_notifs:
        # print(instance)
        message = instance.liker.username + " gefällt einen deiner Beiträge."
        link = (
            "/groups/"
            + str(instance.post.group.id)
            + "/post/"
            + str(instance.post.id)
            + "/"
        )
        signal_id = instance.post.creator.profile.signal_id
        app_id = "56c16a44-f980-41c2-8a74-b4591cc6ab35"
        header = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "app_id": app_id,
            "include_player_ids": [signal_id],
            "contents": {"en": message},
            "url": "https://social-tests.herokuapp.com" + link,
        }
        r = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=header,
            data=json.dumps(payload),
        )
        user = User.objects.get(pk=instance.post.creator.pk)
        notif = Notification.objects.create(
            content=message, user=user, link=link, actor=instance.liker
        )
        # print(r.text)


@receiver(post_save, sender=Comment)
def create_comment(sender, instance, created, **kwargs):
    # print(instance.post.creator.username)
    if (
        created
        and instance.creator.pk != instance.post.creator.pk
        and instance.post.creator.profile.comments_notifs
    ):
        # print(instance)
        message = instance.creator.username + " hat deinen Beitrag kommentiert."
        link = (
            "/groups/"
            + str(instance.post.group.id)
            + "/post/"
            + str(instance.post.id)
            + "/"
        )
        signal_id = instance.post.creator.profile.signal_id
        app_id = "56c16a44-f980-41c2-8a74-b4591cc6ab35"
        header = {"Content-Type": "application/json; charset=utf-8"}
        payload = {
            "app_id": app_id,
            "include_player_ids": [signal_id],
            "contents": {"en": message},
            "url": "https://social-tests.herokuapp.com" + link,
        }
        r = requests.post(
            "https://onesignal.com/api/v1/notifications",
            headers=header,
            data=json.dumps(payload),
        )
        user = User.objects.get(pk=instance.post.creator.pk)
        notif = Notification.objects.create(
            content=message, user=user, link=link, actor=instance.creator
        )
        # print(r.text)
