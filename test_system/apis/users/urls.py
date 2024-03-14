from django.urls import path
from test_system.apis.users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("authenticate/", views.AuthenticatUser.as_view(), name=AuthenticateUser),
    path("", views.UsersGetCreateView.as_view(), name="UsersGetCreateView"),
    path("<uuid:user_id>/", views.UserGetUpdateDeleteView.as_view(), name="UsersGetUpdateDeleteView"),
]