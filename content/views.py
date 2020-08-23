from django.shortcuts import render
import json

import django_filters.rest_framework
from rest_framework import viewsets, filters
from rest_framework_extensions.mixins import NestedViewSetMixin

from content.models import Post, Comment, CommentLike, PostLike, Group, Notification
from content.serializers import (
    PostSerializer,
    CommentSerializer,
    CommentLikeSerializer,
    PostLikeSerializer,
    GroupSerializer,
    NotificationSerializer,
)


class PostViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    # queryset += Post.comment_set.all()
    serializer_class = PostSerializer
    filter_backends = [
        filters.SearchFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    search_fields = ["title"]
    filterset_fields = ["title"]


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["comment_content"]


class GroupViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [filters.SearchFilter]
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
