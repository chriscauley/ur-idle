from django.apps import apps
from django.core.management.commands.makemigrations import Command as OriginalCommand


IGNORED_MISSING_MIGRATIONS = {
    'sessions',
    'messages',
    'contenttypes',
    'admin',
    'auth',
    'staticfiles',
    'mailer',
}


class Command(OriginalCommand):
    def handle(self, *app_labels, **options):
        if app_labels:
            return super().handle(*app_labels, **options)

        app_labels = {cfg.label for cfg in apps.get_app_configs()} - IGNORED_MISSING_MIGRATIONS
        return super().handle(*app_labels, **options)