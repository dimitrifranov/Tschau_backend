from django.contrib import admin

# Register your models here.

from content.models import Post, Comment, Group, Membership, Notification, PostLike

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Group)
admin.site.register(Membership)
admin.site.register(Notification)
admin.site.register(PostLike)
