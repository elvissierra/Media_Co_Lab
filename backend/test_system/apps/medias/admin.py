from django.contrib import admin
from test_system.apps.medias.models import Medias

# Register your models here.
admin.site.register(Medias)


class MediasAdmin(admin.ModelAdmin):
    list_display = ""
    list_filter = "title"
    search_fields = "title"
