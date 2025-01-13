from django.urls import path
from test_system.apis.comments import views

urlpatterns = [
    path("", views.CommentsGetOrCreateView.as_view(), name="CommentsGetOrCreate"),
    path("<uuid:comment_id>/", views.CommentGetUpdateDeleteView.as_view(), name="CommentsGetUpdateDelete"),
    path("<uuid:medias_id>/comments/", views.CommentsGetOrCreateView.as_view(), name="CommentsGetOrCreateView"),
]