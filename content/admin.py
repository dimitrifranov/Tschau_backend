from django.contrib import admin

# Register your models here.

from content.models import Post, Comment, Group

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Group)
