from django.contrib.auth.models import User, Group
from authentication.models import Follow
from content.models import Post
from django.db.models import Q


from authentication.serializers import (
    UserSerializer,
    FollowSerializer,
)
from content.serializers import PostSerializer

from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


# Create your views here.
class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["username"]


class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class FollowViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FollowDetails(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class UserPostList(generics.ListAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        pk = self.kwargs["pk"]
        user_id = self.request.query_params.get("user")
        posts = set()
        if not user_id:
            is_by_user = Q(creator__pk=pk)
            is_public = Q(group__public=True)
            return Post.objects.filter(is_by_user & is_public)
        # else:
        #     user = User.objects.get(pk=user_id)
