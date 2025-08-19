from django.apps import AppConfig


class CatalogoProductosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogo_productos'

    def ready(self):
        import catalogo_productos.signals
