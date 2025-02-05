from django.urls import path
from . import views

urlpatterns = [
    path("", views.ChatsGetView.as_view(), name="ChatsGetOrCreate"),
    path("<uuid:chat_id>/", views.ChatGetUpdateDeleteView.as_view(), name="ChatGetUpdateDelete"),
]