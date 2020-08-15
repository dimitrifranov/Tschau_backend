from django.contrib.auth.models import User, Group
from authentication.models import Follow
from content.models import Post

from authentication.serializers import (
    UserSerializer,
    GroupSerializer,
    FollowSerializer,
)
from content.serializers import PostSerializer

from rest_framework import generics, permissions, filters

# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


# Create your views here.
class UserList(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]


class UserDetails(generics.RetrieveUpdateAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ["groups"]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FollowDetails(generics.RetrieveDestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class UserPostList(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()

     def get_queryset(self):
        pk = self.kwargs['pk']
        return Post.objects.filter(creator__pk=pk)
