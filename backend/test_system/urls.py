from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from test_system.apis.users.views import LoginView
from knox import views as knox_views
from test_system import swagger
from django.shortcuts import redirect

def redirect_to_docs(request):
    return redirect("api/schema/swagger-ui/")

urlpatterns = [
    path("", redirect_to_docs),
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
