from django.contrib.auth.models import User, Group
from authentication.models import Follow

from authentication.serializers import (
    UserSerializer,
    GroupSerializer,
    FollowSerializer,
)

from rest_framework import generics, permissions

# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope


# Create your views here.
class UserList(generics.ListCreateAPIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
