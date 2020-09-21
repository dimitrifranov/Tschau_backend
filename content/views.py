from django.shortcuts import render
import json
import re

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

    def get_queryset(self):
        if not self.request.query_params.get("user"):
            return Post.objects.none()
        data = self.request.query_params.get("user")
        group_id = re.findall("\d", self.request.path_info)[0]
        # print(group_id)
        # print(data)
        # data_dict = json.loads(data)
        user = User.objects.get(pk=data)
        group = Group.objects.get(id=group_id)
        # print(user)
        if group.public:
            return group.posts.all()
        if len(user.joined_groups.all()):
            if user.joined_groups.filter(user=user):
                return group.posts.all()
        return Post.objects.none()


class GroupsPostsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
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
        if not self.request.query_params.get("user"):
            return Post.objects.none()
        data = self.request.query_params.get("user")
        user = User.objects.get(pk=data)
        posts = set()
        public_groups = Group.objects.filter(public=True)
        for public_group in public_groups.all():
            for post in public_group.posts.all():
                posts.add(post.id)
        if len(user.joined_groups.all()):
            for joined_group in user.joined_groups.filter(group__public=False):
                print(joined_group)
                for post in joined_group.group.posts.all():
                    posts.add(post.id)
        return Post.objects.filter(id__in=posts)


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

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

