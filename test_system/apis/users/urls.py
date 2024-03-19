from django.urls import path
from test_system.apis.users import views

urlpatterns = [
    path("", views.UsersGetCreateView.as_view(), name="UsersGetCreateView"),
    path("<uuid:user_id>/", views.UserGetUpdateDeleteView.as_view(), name="UsersGetUpdateDeleteView"),
]