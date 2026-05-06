from django.urls import path
from test_system.apis.users.views import (
    UsersGetView, UserCreateView, UserGetPatchDeleteView,
    UserApproveView, UserDenyView, CurrentUserView,
)

urlpatterns = [
    path("", UsersGetView.as_view(), name="UsersGetView"),
    path("me/", CurrentUserView.as_view(), name="CurrentUserView"),
    path("create/", UserCreateView.as_view(), name="UserCreateView"),
    path(
        "<uuid:user_id>/",
        UserGetPatchDeleteView.as_view(),
        name="UsersGetPatchDeleteView",
    ),
    path(
        "<uuid:user_id>/approve/",
        UserApproveView.as_view(),
        name="UserApproveView",
    ),
    path(
        "<uuid:user_id>/deny/",
        UserDenyView.as_view(),
        name="UserDenyView",
    ),
]
