from rest_framework import serializers
from content.models import (
    Post,
    Comment,
    CommentLike,
    PostLike,
    Group,
    Notification,
    Membership,
)
from django.contrib.auth.models import User

# from authentication.serializers import UserSerializer

# try:
#     from authentication.serializers import UserSerializer
# except ImportError:
#     import sys

#     UserSerializer = sys.modules[__package__ + ".UserSerializer"]


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = "__all__"


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):

    likes = CommentLikeSerializer(many=True, read_only=True)
    creator_name = serializers.CharField(source="creator.username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    likes = PostLikeSerializer(many=True, read_only=True)
    creator_name = serializers.CharField(source="creator.username", read_only=True)
    group_name = serializers.CharField(source="group.name", read_only=True)
    profile_pic = serializers.FileField(
        source="creator.profile.profile_picture", read_only=True
    )

    class Meta:
        model = Post
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):

    # posts = PostSerializer(many=True, read_only=True)
    creator_name = serializers.CharField(source="creator.username", read_only=True)
    group_members = MembershipSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    profile_pic = serializers.FileField(
        source="user.profile.profile_picture", read_only=True
    )

    class Meta:
        model = Notification
        fields = "__all__"
