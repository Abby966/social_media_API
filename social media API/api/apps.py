from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        from . import signals  # noqa


class PiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pi'
