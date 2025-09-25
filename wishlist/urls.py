from django.urls import path
from .views import wishlist_view, add_to_wishlist, remove_from_wishlist

app_name = 'wishlist'

urlpatterns = [
    path('', wishlist_view, name='list'),
    path('add/<int:product_id>/', add_to_wishlist, name='add'),
    path('remove/<int:product_id>/', remove_from_wishlist, name='remove'),
]