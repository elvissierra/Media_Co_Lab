from django.urls import path
from test_system.apis.organizations import views

urlpatterns = [
    path("", views.OrganizationsGetView.as_view(), name="OrganizationsGetView"),
    path("ov/", views.UserOrganizationView.as_view(), name="UserOganization"),
    path(
        "register/",
        views.OrganizationCreateView.as_view(),
        name="OrganizationCreateView",
    ),
    path("demo/", views.DemoOrgCreateView.as_view(), name="DemoOrgCreateView"),
    path("pending/", views.PendingOrganizationsView.as_view(), name="PendingOrganizationsView"),
    path(
        "<uuid:organization_id>/",
        views.OrganizationGetUpdateDeleteView.as_view(),
        name="OrganizationsGetUpdateDeleteView",
    ),
    path(
        "<uuid:organization_id>/approve/",
        views.OrganizationApproveView.as_view(),
        name="OrganizationApproveView",
    ),
    path(
        "<uuid:organization_id>/deny/",
        views.OrganizationDenyView.as_view(),
        name="OrganizationDenyView",
    ),
]
