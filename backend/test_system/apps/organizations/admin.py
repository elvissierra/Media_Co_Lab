from django.contrib import admin
from test_system.apps.organizations.models import Organization

# Register your models here.
admin.site.register(Organization)


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("title", "is_approved")
    list_filter = "is_approved"
    search_fields = "title"
