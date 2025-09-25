from django.apps import AppConfig


class PoushiaProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'poushia_products'
    verbose_name = 'مدیریت محصولات'


    def ready(self):
        import poushia_products.signals

