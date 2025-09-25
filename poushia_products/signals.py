from django.db.models.signals import post_delete
from django.dispatch import receiver
from poushia_products.models import Product
from wishlist.models import Wishlist
from styleboard.models import StyleBoard
from poushia_order.models import OrderDetail

@receiver(post_delete, sender=Product)
def cleanup_related_data(sender, instance, **kwargs):
    # حذف از علاقه‌مندی‌ها
    Wishlist.objects.filter(products=instance).update(products=models.F('products').remove(instance))

    # حذف از استایل‌ساز
    StyleBoard.objects.filter(products=instance).update(products=models.F('products').remove(instance))

    # حذف از جزئیات سفارش
    OrderDetail.objects.filter(product=instance).delete()