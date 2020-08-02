from django.urls import path, include

from content import views
from rest_framework_extensions.routers import ExtendedDefaultRouter as DefaultRouter

router = DefaultRouter()

router.register(r"notifications", views.NotificationViewSet, basename="notification")
groups_routes = router.register(r"groups", views.GroupViewSet, basename="group")
posts_routes = groups_routes.register(
    r"posts", views.PostViewSet, basename="post", parents_query_lookups=["group"]
)

posts_routes.register(
    r"comments",
    views.CommentViewSet,
    basename="comment",
    parents_query_lookups=["post__group", "post"],
).register(
    r"likes",
    views.CommentLikeViewSet,
    basename="commentLike",
    parents_query_lookups=["comment__post__group", "comment__post", "comment"],
)

posts_routes.register(
    r"likes",
    views.PostLikeViewSet,
    basename="postLike",
    parents_query_lookups=["post__group", "post"],
)

urlpatterns = router.urls
