from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tutoringApp.apps.accounts"
    label = "accounts"

    def ready(self):
        import tutoringApp.apps.accounts.signals  # noqa: F401
