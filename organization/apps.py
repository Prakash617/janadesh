from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'  # optional but recommended
    name = 'organization'

    def ready(self):
        # Import signals when the app is ready
        import organization.signals
