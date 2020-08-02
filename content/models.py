from django.db import models

from django.utils.translation import gettext as _
from django.urls import reverse
from django.contrib.auth.models import User


class Post(models.Model):

    # pub_date = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)
    title = models.CharField(_("Title"), max_length=50)
    creator = models.ForeignKey(
        User, verbose_name=_("creator"), related_name="posts", on_delete=models.CASCADE,
    )
    # likes = models.CharField(_("likes"), max_length=50)
    src = models.FileField(_("file"), upload_to="static", max_length=100)
    group = models.ForeignKey(
        "content.Group",
        verbose_name=_("groups"),
        related_name=_("posts"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _("post")
        verbose_name_plural = _("posts")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):

    comment_content = models.CharField(_("content"), max_length=100)
    creator = models.ForeignKey(
        User,
        verbose_name=_("creator"),
        related_name="comments",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        "content.Post", related_name=_("comments"), on_delete=models.CASCADE
    )
    reply_to = models.ForeignKey(
        "content.Comment",
        verbose_name=_("replies_to"),
        related_name=_("replies"),
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # pub_date = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return self.comment_content

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})


class CommentLike(models.Model):

    liker = models.ForeignKey(
        User,
        verbose_name=_("liker"),
        related_name="liked_comments",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        "content.Comment", related_name=_("likes"), on_delete=models.CASCADE
    )
    # pub_date = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("commentlike")
        verbose_name_plural = _("commentlikes")

    # def __str__(self):
    #     return self.liker_name

    def get_absolute_url(self):
        return reverse("commentlike_detail", kwargs={"pk": self.pk})


class PostLike(models.Model):

    liker = models.ForeignKey(
        User,
        verbose_name=_("liker"),
        related_name="liked_posts",
        on_delete=models.CASCADE,
    )
    post = models.ForeignKey(
        "content.Post", related_name=_("likes"), on_delete=models.CASCADE
    )
    pub_date = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("postlike")
        verbose_name_plural = _("postlikes")

    # def __str__(self):
    #     return self.liker_name

    def get_absolute_url(self):
        return reverse("postlike_detail", kwargs={"pk": self.pk})


class Group(models.Model):

    creator = models.ForeignKey(
        User,
        verbose_name=_("creator"),
        related_name="created_groups",
        on_delete=models.CASCADE,
    )
    # pub_date = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)
    name = models.CharField(_("name"), max_length=50, unique=True)
    description = models.CharField(_("description"), max_length=100)

    class Meta:
        verbose_name = _("group")
        verbose_name_plural = _("groups")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("group_detail", kwargs={"pk": self.pk})


class Notification(models.Model):

    content = models.CharField(_("content"), max_length=50)
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    time = models.DateTimeField(_("created"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("notification")
        verbose_name_plural = _("notifications")

    def __str__(self):
        return self

    def get_absolute_url(self):
        return reverse("notification_detail", kwargs={"pk": self.pk})
