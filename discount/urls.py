from django.urls import path
from .views import apply_discount

urlpatterns = [
    path('apply/', apply_discount, name='apply_discount'),
]