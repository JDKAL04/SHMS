# accounts/apps.py

from django.apps import AppConfig

class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "User Accounts"

    def ready(self):
        # Import signal handlers
        import accounts.signals
