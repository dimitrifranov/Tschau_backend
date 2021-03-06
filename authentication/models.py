from django.db import models
from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserProfile(models.Model):

    user = models.OneToOneField(
        User, verbose_name=_("User"), related_name=("profile"), on_delete=models.CASCADE
    )
    bio = models.CharField(_("bio"), max_length=500, blank=True, null=True)
    birth_date = models.DateField(
        _("Birth_date"), auto_now=False, auto_now_add=False, blank=True, null=True
    )
    profile_picture = models.FileField(
        _("Profile Pictures"),
        upload_to="profile_picture",
        max_length=100,
        blank=True,
        null=True,
    )
    signal_id = models.CharField(_("id"), max_length=50, blank=True, null=True)
    new_follow_notifs = models.BooleanField(
        _("new follower notifications"), default=True
    )
    follow_post_notifs = models.BooleanField(
        _("follower post notifications"), default=True
    )
    like_notifs = models.BooleanField(_("like notifications"), default=True)
    comments_notifs = models.BooleanField(_("comments notifications"), default=True)

    class Meta:
        verbose_name = _("userprofile")
        verbose_name_plural = _("userprofiles")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("userprofile_detail", kwargs={"pk": self.pk})


class Follow(models.Model):

    user_from = models.ForeignKey(
        User, related_name=_("following"), on_delete=models.CASCADE
    )
    user_to = models.ForeignKey(
        User, related_name=_("follower"), on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("follow")
        verbose_name_plural = _("follows")

    def __str__(self):
        return "{} follows {}".format(self.user_from, self.user_to)

    def get_absolute_url(self):
        return reverse("follow_detail", kwargs={"pk": self.pk})

