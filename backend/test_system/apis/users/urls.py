from django.urls import path
from test_system.apis.users import views

urlpatterns = [
    path("", views.UsersGetView.as_view(), name="UsersGetView"),
    path("create/", views.UserCreateView.as_view(), name="UserCreateView"),
    path("<uuid:user_id>/", views.UserGetPatchDeleteView.as_view(), name="UsersGetPatchDeleteView"),
]