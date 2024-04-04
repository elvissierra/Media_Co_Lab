from django.urls import path
from test_system.apis.users import views

urlpatterns = [
    path("", views.UserCreateView.as_view(), name="UserCreateView"),
    path("<uuid:user_id>/", views.UserGetUpdateDeleteView.as_view(), name="UsersGetUpdateDeleteView"),
]