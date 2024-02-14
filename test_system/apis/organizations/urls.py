from django.urls import path
from test_system.apis.organizations import views

urlpatterns = [
    path("", views.OrganizationsGetCreateView.as_view(), name="OrganizationsGetCreateView"),
    path("<uuid:organization_id>/", views.OrganizationGetUpdateDeleteView.as_view(), name="OrganizationsGetUpdateDeleteView"),
]