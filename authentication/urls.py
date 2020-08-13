from django.urls import path, include

from authentication import views

urlpatterns = [
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<pk>/", views.UserDetails.as_view(), name="user-detail"),
    path("follow/", views.FollowViewSet.as_view(), name="follow-list")
    path("follow/<pk>/", views.FollowDetails.as_view(), name="follow-detail")
    # path("groups/", views.GroupList.as_view(), name="group-list"),
]
