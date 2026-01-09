from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    name = 'apps.categories'

    def ready(self) -> None:
        from apps.categories import translation  # noqa: F401
