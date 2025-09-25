import os
import random

from django.db import models
from django.db.models import Q

from poushia_products_category.models import ProductCategory


# Create your models here.
def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image(instance, filename):
    rand_name = random.randint(1, 99999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{instance.id}-{rand_name}{ext}"
    return f"products/{final_name}"


def upload_image_gallery(instance, filename):
    rand_name = random.randint(1, 99999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{instance.id}-{rand_name}{ext}"
    return f"gallery/{final_name}"


# مدل سایز
class Size(models.Model):
    title = models.CharField(max_length=50, verbose_name='سایز')

    class Meta:
        verbose_name = 'سایز'
        verbose_name_plural = 'سایز'

    def __str__(self):
        return self.title


# مدل رنگ
class Color(models.Model):
    title = models.CharField(max_length=50, verbose_name='رنگ')

    class Meta:
        verbose_name = 'رنگ'
        verbose_name_plural = 'رنگ'

    def __str__(self):
        return self.title


# مدیریت محصولات
class ProductManager(models.Manager):
    def get_active_products(self):
        return self.get_queryset().filter(active=True)

    def get_product_by_id(self, product_id):
        qs = self.get_queryset().filter(id=product_id, active=True)
        if qs.count() == 1:
            return qs.first()
        else:
            return None

    def search_products(self, query):
        lookup = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(tag__title__icontains=query)
        )
        return self.get_queryset().filter(lookup, active=True).distinct()

    def get_product_by_category(self, category_name):
        return self.get_queryset().filter(category__name__iexact=category_name)


class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    price = models.DecimalField(decimal_places=2, max_digits=15, verbose_name='قیمت')
    brand = models.CharField(max_length=100, default="نامشخص", verbose_name="برند")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    rating = models.FloatField(default=0.0, verbose_name="امتیاز خرید")
    image = models.ImageField(upload_to=upload_image, null=True, blank=True, verbose_name='تصویر')
    active = models.BooleanField(default=False, verbose_name='فعال/غیرفعال')
    time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(ProductCategory, blank=True, verbose_name='دسته بندی')
    featured = models.BooleanField(default=False, verbose_name='محصول ویژه')
    sizes = models.ManyToManyField(Size, verbose_name='سایزها', blank=True)
    colors = models.ManyToManyField(Color, verbose_name='رنگ‌ها', blank=True)
    visits = models.IntegerField(default=0,verbose_name='تعداد مشاهده')

    objects = ProductManager()

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def __str__(self):
        return self.title

    def get_product_detail_url(self):
        return f"/products/{self.id}/{self.title.replace(' ', '_')}"


class ProductGallery(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    image = models.ImageField(upload_to=upload_image_gallery, null=True, blank=True, verbose_name='تصویر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='انتخاب محصول')

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'گالری تصاویر'

    def __str__(self):
        return self.title
