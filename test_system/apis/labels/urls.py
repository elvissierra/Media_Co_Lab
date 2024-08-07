from django.urls import path
from test_system.apis.labels import views

urlpatterns = [
    path("", views.LabelsGetCreateView.as_view(), name="LabelsGetCreateView"),
    path("<uuid:label_id>/", views.LabelGetUpdateDeleteView.as_view(), name="LabelsGetUpdateDeleteView",),
    ]
