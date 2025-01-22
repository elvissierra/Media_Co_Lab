from django.urls import path
from . import views

urlpatterns = [
    path("", views.CommentsGetOrCreateView.as_view(), name="CommentsGetOrCreate"),
    path("<uuid:comment_id>/", views.CommentGetUpdateDeleteView.as_view(), name="CommentsGetUpdateDelete"),
]