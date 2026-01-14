from django.apps import AppConfig


class OrganizationAppConfig(AppConfig):
    name = 'organization_app'
    
    def ready(self):
        import organization_app.signals  # noqa
