from django.contrib.auth.models import User
from django.db import models

from poushia_products.models import Product, Color, Size  # اضافه شدن Color و Size


# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده/نشده')
    pay_date = models.DateTimeField(null=True)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    def __str__(self):
        return self.user.get_full_name()

    def total_price(self):
        amount = 0
        for detail in self.orderdetail_set.all():
            amount += detail.price * detail.count
        return amount


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,verbose_name='نام مشتری')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name='نام محصول')
    count = models.IntegerField(verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت')
    selected_color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='رنگ انتخابی')
    selected_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='سایز انتخابی')

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'جزئیات سبد های خرید'

    def __str__(self):
        return self.product.title

    def product_sum_in_cart(self):
        return self.price * self.count