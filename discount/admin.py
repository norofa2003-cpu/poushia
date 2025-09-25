from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DiscountCode


@admin.register(DiscountCode)
class DiscountCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_percent', 'used_count', 'usage_limit', 'is_active', 'expires_at']
    list_filter = ['is_active']
    search_fields = ['code']

