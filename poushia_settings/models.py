import os
import random

from django.db import models

# Create your models here.


def get_file_extension(file):
    base_name = os.path.basename(file)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image(instance, filename):
    rand_name = random.randint(1, 99999999999999)
    name, ext = get_file_extension(filename)
    final_name = f"{rand_name}{ext}"
    return f"setting/{final_name}"


class Settings(models.Model):
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=200,verbose_name='تلفن ثابت')
    mobile = models.CharField(max_length=200,verbose_name='شماره تماس')
    fax = models.CharField(max_length=200,verbose_name='فکس')
    address = models.CharField(max_length=250,verbose_name='آدرس')
    copyright = models.CharField(max_length=250,verbose_name='کپی رایت')
    about = models.TextField(verbose_name='درباره ما')
    instagram = models.URLField(verbose_name='ادرس اینستاگرام')
    telegram = models.URLField(verbose_name='ادرس تلگرام')
    logo = models.ImageField(upload_to=upload_image, null=True, blank=True, verbose_name='تصویر')

    class Meta:
        verbose_name='تنظیمات'
        verbose_name_plural='تنظیمات'

    def __str__(self):
         return 'تنظیمات سایت'

