from django.apps import AppConfig


class MainAppConfig(AppConfig):
    name = 'main_app'

    def ready(self):
        # import signal handlers
        import main_app.signals