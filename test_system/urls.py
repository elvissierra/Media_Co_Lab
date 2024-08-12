"""
URL configuration for test_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from test_system.apis.users.views import LoginView
from knox import views as knox_views
from test_system import swagger

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", LoginView.as_view(), name="knox_login"),
    path("api/auth/logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("api/auth/logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path("api/users/", include("test_system.apis.users.urls")),
    path("api/teams/", include("test_system.apis.teams.urls")),
    path("api/organizations/", include("test_system.apis.organizations.urls")),
    path("api/labels/", include("test_system.apis.labels.urls")),
    path("api/medias/", include("test_system.apis.medias.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.extend(swagger.urlpatterns)
