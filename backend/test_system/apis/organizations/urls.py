from django.urls import path
from test_system.apis.organizations import views

urlpatterns = [
    path("", views.OrganizationsGetView.as_view(), name="OrganizationsGetView"),
    path("ov/", views.UserOrganizationView.as_view(), name="UserOganization"),
    path("create/", views.OrganizationCreateView.as_view(), name="OrganizationCreateView"),
    path("<uuid:organization_id>/", views.OrganizationGetUpdateDeleteView.as_view(), name="OrganizationsGetUpdateDeleteView"),
]