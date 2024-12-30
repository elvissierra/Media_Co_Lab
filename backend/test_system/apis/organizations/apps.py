from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_system.apps.organizations'

    def ready(self):
        import test_system.apps.organizations.signals