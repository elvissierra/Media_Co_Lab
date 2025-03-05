from django.urls import path
from test_system.apis.teams import views

urlpatterns = [
    path("", views.TeamsGetCreateView.as_view(), name="TeamsGetCreateView"),
    path(
        "<uuid:team_id>/",
        views.TeamGetUpdateDeleteView.as_view(),
        name="TeamsGetUpdateDeleteView",
    ),
    path(
        "<uuid:team_id>/medias/",
        views.TeamMediasGetView.as_view(),
        name="TeamMediasGetView",
    ),
]
