from django.contrib import admin
from .models import Product, ProductGallery, Size, Color

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'title', 'price', 'active', 'featured']
    filter_horizontal = ['sizes', 'colors']

    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductGallery)
admin.site.register(Size)
admin.site.register(Color)