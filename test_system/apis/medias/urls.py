from django.urls import path
from . import views

urlpatterns = [
    path("", views.MediasGetCreateView.as_view(), name="MediasGetCreateView"),
    path("<uuid:medias_id>/", views.MediasGetCreateView.as_view(), name="MediasGetCreateView"),
]