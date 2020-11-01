from django.shortcuts import render
import json
import re

import django_filters.rest_framework
from rest_framework import viewsets, filters
from rest_framework_extensions.mixins import NestedViewSetMixin

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


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
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        django_filters.rest_framework.DjangoFilterBackend,
    ]
    search_fields = ["title"]
    ordering_fields = ["pub_date", "likes"]

    def get_queryset(self):
        group_id = int(self.kwargs["parent_lookup_group"])
        if "pk" in self.kwargs:
            post_id = int(self.kwargs["pk"])
        else:
            post_id = None
        group = Group.objects.get(id=group_id)
        # print(group_id)
        if not self.request.query_params.get("user"):
            if group.public:
                if post_id:
                    return group.posts.filter(id=post_id)
                return group.posts.all()
            else:
                return Post.objects.none()
        data = int(self.request.query_params.get("user"))

        user = User.objects.get(pk=data)
        # print(data)
        # print(group.creator.pk)
        if group.public or group.creator.pk == data:
            if post_id:
                # print(post_id)
                return group.posts.filter(id=post_id)
            return group.posts.all()
        if len(group.group_members.all()):
            if group.group_members.filter(user=user):
                if post_id:
                    return group.posts.filter(id=post_id)
                return group.posts.all()
        return Post.objects.none()


class PublicPostsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title"]
    ordering_fields = ["pub_date", "likes"]

    def get_queryset(self):
        posts = set()
        public_groups = Group.objects.filter(public=True)
        for public_group in public_groups.all():
            for post in public_group.posts.all():
                posts.add(post.id)
        return Post.objects.filter(id__in=posts)


class GroupsPostsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
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
                for post in joined_group.group.posts.all():
                    posts.add(post.id)
        return Post.objects.filter(id__in=posts)


class FeedViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
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
        user_id = self.request.query_params.get("user")
        user = User.objects.get(pk=user_id)
        posts = set()
        if len(user.posts.all()):
            for post in user.posts.all():
                posts.add(post.id)
        if len(user.joined_groups.all()):
            for joined_group in user.joined_groups.filter(group__public=False):
                for post in joined_group.group.posts.all():
                    posts.add(post.id)
        # print(user.following.all())
        if len(user.following.all()):
            for following_user in user.following.all():
                for post in following_user.user_to.posts.all():
                    if post.group.public:
                        posts.add(post.id)

        return Post.objects.filter(id__in=posts)


class CommentViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["comment_content"]


class GroupViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["name"]

    def get_queryset(self):
        group_id = (
            re.findall("(?<=\/groups\/)\d+", self.request.path_info)[0]
            if len(re.findall("(?<=\/groups\/)\d+", self.request.path_info))
            else 0
        )
        user_id = self.request.query_params.get("user")
        if group_id:
            group = Group.objects.get(id=group_id)
            if group.public:
                return Group.objects.filter(id=group_id)
            elif user_id:
                user = User.objects.get(pk=user_id)
                for group_member in group.group_members.all():
                    if group_member.user.id == int(user_id):
                        return Group.objects.filter(id=group_id)
                for created_group in user.created_groups.all():
                    if created_group.id == int(group_id):
                        return Group.objects.filter(id=group_id)
                return Group.objects.none()
            else:
                return Group.objects.none()
        else:
            groups = set()
            public_groups = Group.objects.filter(public=True)
            for public_group in public_groups.all():
                groups.add(public_group.id)
            if user_id:
                user = User.objects.get(pk=user_id)
                for joined_group in user.joined_groups.all():
                    groups.add(joined_group.group.id)
                for created_group in user.created_groups.all():
                    groups.add(created_group.id)
            return Group.objects.filter(id__in=groups)

            return Post.objects.filter(id__in=posts)


class CommentLikeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer


class PostLikeViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    filter_backends = [
        filters.OrderingFilter,
    ]
    ordering_fields = ["time"]

    def get_queryset(self):
        user = self.request.query_params.get("user")
        # data_dict = json.loads(data)
        # print(data_dict["user"])
        return Notification.objects.filter(user=user)


class MembershipViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
