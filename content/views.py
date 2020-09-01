from django.shortcuts import render
import json

import django_filters.rest_framework
from rest_framework import viewsets, filters
from rest_framework_extensions.mixins import NestedViewSetMixin

from content.models import (
    Post,
    Comment,
    CommentLike,
    PostLike,
    Group,
    Notification,
    Membership,
)
from authentication.models import User
from content.serializers import (
    PostSerializer,
    CommentSerializer,
    CommentLikeSerializer,
    PostLikeSerializer,
    GroupSerializer,
    NotificationSerializer,
    MembershipSerializer,
)


class PostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    # queryset += Post.comment_set.all()
    serializer_class = PostSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    search_fields = ["title"]
    ordering_fields = ["pub_date", "likes"]


class FeedViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    # queryset += Post.comment_set.all()
    serializer_class = PostSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title"]
    ordering_fields = ["pub_date", "likes"]

    def get_queryset(self):
        data = self.request.query_params.get("user")
        # print(data)
        # data_dict = json.loads(data)
        user = User.objects.get(pk=data)
        # print(user)
        posts = set()
        for following in user.following.all():
            for post in following.user_to.posts.all():
                posts.add(post.id)
                # print(posts)
        return Post.objects.filter(id__in=posts)


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["comment_content"]


class GroupViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name"]


class CommentLikeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer


class PostLikeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        data = self.request.query_params.get("data")
        data_dict = json.loads(data)
        # print(data_dict["user"])
        return Notification.objects.filter(user=data_dict["user"])


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer

