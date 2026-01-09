from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'apps.products'

    def ready(self) -> None:
        from apps.products import translation  # noqa: F401
        from apps.products import signals  # noqa: F401
