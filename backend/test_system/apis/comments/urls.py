from django.urls import path
from . import views

urlpatterns = [
    path("", views.CommentsGetView.as_view(), name="CommentsGetOrCreate"),
    path("<uuid:comment_id>/", views.CommentGetUpdateDeleteView.as_view(), name="CommentsGetUpdateDelete"),
]