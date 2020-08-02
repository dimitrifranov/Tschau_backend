from django.contrib.auth.models import User, Group

from rest_framework import serializers
from dj_rest_auth.serializers import UserDetailsSerializer

from django.contrib.auth.hashers import make_password

from authentication.models import Follow

# from content.serializers import PostSerializer

# from authentication.serializers import FollowSerializer


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"


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
    # posts = PostSerializer(many=True, read_only=True)
    following = FollowSerializer(many=True, read_only=True)
    follower = FollowSerializer(many=True, read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        model = User
        fields = UserDetailsSerializer.Meta.fields + (
            "password",
            "bio",
            "birth_date",
            "profile_picture",
            # "posts",
            "signal_id",
            "following",
            "follower",
        )
        # depth = 1
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        validated_data["password"] = make_password(validated_data["password"])
        user = super(UserSerializer, self).create(validated_data)

        return user

    # def update(self, instance, validated_data):
    #     profile_data = validated_data.pop("profile", None)
    #     return super(UserSerializer, self).update(instance, validated_data)

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        bio = profile_data.get("bio")
        birth_date = profile_data.get("birth_date")
        profile_picture = profile_data.get("profile_picture")
        signal_id = profile_data.get("signal_id")

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
        profile.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
