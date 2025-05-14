from django.apps import AppConfig


class SecuritycheckConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'securityCheck'

    def ready(self):
        import securityCheck.signals
