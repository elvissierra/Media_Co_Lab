from django.contrib import admin
from test_system.apps.users.models import CustomUser

# Register your models here.
admin.site.register(CustomUser)
