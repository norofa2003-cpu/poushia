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
    final_name = f"{instance.id}-{rand_name}{ext}"
    return f"products/{final_name}"



class Slider(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان اسلایدر')
    link = models.URLField(max_length=200 ,verbose_name='لینک ')
    description = models.TextField(verbose_name='توضیحات')
    image = models.ImageField(upload_to=upload_image,null=True,blank=True ,verbose_name='تصویر')


    class Meta:
        verbose_name ='اسلایدر'
        verbose_name_plural ='اسلایدرها'

    def __str__(self):
        return self.title