from django.apps import AppConfig


class WebToolConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "web_tool"
    def ready(self):
        import web_tool.signals  # 替換為你的應用名稱

