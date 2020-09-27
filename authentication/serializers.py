from django.contrib.auth.models import User

from rest_framework import serializers

# from dj_rest_auth.serializers import UserDetailsSerializer
from content.serializers import MembershipSerializer

from django.contrib.auth.hashers import make_password

from authentication.models import Follow

# from content.serializers import PostSerializer

# from authentication.serializers import FollowSerializer


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"


# class GroupSerializer(serializers.ModelSerializer):
#     members = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

#     class Meta:
#         model = Group
#         fields = ("name", "members")


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = User
        fields = ("pk", "username", "email", "first_name", "last_name")


class UserSerializer(UserDetailsSerializer):
    bio = serializers.CharField(source="profile.bio", required=False, allow_null=True)
    birth_date = serializers.DateField(
        source="profile.birth_date", required=False, allow_null=True
    )
    profile_picture = serializers.ImageField(
        source="profile.profile_picture", required=False, allow_null=True
    )
    signal_id = serializers.CharField(
        source="profile.signal_id", required=False, allow_null=True
    )
    follow_post_notifs = serializers.BooleanField(source="profile.follow_post_notifs")
    new_follow_notifs = serializers.BooleanField(source="profile.new_follow_notifs")
    like_notifs = serializers.BooleanField(source="profile.like_notifs")
    comments_notifs = serializers.BooleanField(source="profile.comments_notifs")
    follower = FollowSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)
    joined_groups = MembershipSerializer(many=True, read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
            "password",
            "bio",
            "birth_date",
            "profile_picture",
            "signal_id",
            "following",
            "follower",
            "joined_groups",
            "follow_post_notifs",
            "new_follow_notifs",
            "like_notifs",
            "comments_notifs",
        )
        extra_kwargs = {
            "password": {"required": False},
        }

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        validated_data["password"] = make_password(validated_data["password"])
        user = super(UserSerializer, self).create(validated_data)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        if len(validated_data["password"]) < 70:
            validated_data["password"] = make_password(validated_data["password"])
        bio = profile_data.get("bio")
        birth_date = profile_data.get("birth_date")
        profile_picture = profile_data.get("profile_picture")
        signal_id = profile_data.get("signal_id")
        comments_notifs = profile_data.get("comments_notifs")
        like_notifs = profile_data.get("like_notifs")
        follow_post_notifs = profile_data.get("follow_post_notifs")
        new_follow_notifs = profile_data.get("new_follow_notifs")

        instance = super(UserSerializer, self).update(instance, validated_data)
        # get and update user profile
        # profile = instance.userprofile
        profile = instance.profile

        # try:
        #     profile = instance.profile
        # except UserProfile.DoesNotExist:
        #     profile = UserProfile()

        if profile_data and bio:
            profile.bio = bio

        if profile_data and signal_id:
            profile.signal_id = signal_id

        if profile_data and birth_date:
            profile.birth_date = birth_date
        if profile_data and profile_picture:
            profile.profile_picture = profile_picture

        if profile_data:
            profile.new_follow_notifs = new_follow_notifs
        if profile_data:
            profile.follow_post_notifs = follow_post_notifs
        if profile_data:
            profile.like_notifs = like_notifs
        if profile_data:
            profile.comments_notifs = comments_notifs

        profile.save()
        return instance

