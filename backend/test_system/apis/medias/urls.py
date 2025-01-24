from django.urls import path
from . import views

urlpatterns = [
    path("", views.MediasGetCreateView.as_view(), name="MediasGetCreateView"),
    path("<uuid:medias_id>/", views.MediasGetUpdateDeleteView.as_view(), name="MediasGetUpdateDeleteView"),
    path("<uuid:medias_id>/comments/", views.MediaCommentsGetCreateView.as_view(), name="MediaCommentsGetCreateView"),
]