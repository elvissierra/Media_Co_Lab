from django.urls import path
from test_system.apis.medias import views

urlpatterns = [
    path("", views.MediasGetCreateView.as_view(), name="MediasGetCreateView"),
    path("<uuid:medias_id>/", views.MediasGetCreateView.as_view(), name="MediasGetCreateView"),
]