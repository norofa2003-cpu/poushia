from django.db import models
from django.contrib.auth.models import User
from poushia_products.models import Product

class StyleBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)