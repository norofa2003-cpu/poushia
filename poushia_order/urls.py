from django.urls import path
from poushia_order.views import add_new_order,cart,verify,send_request,remove_cart_item
app_name = 'poushia_order'

urlpatterns = [
    path('add-new-order', add_new_order,name='add_new_order'),
    path('cart', cart, name='cart'),
    path('remove-cart-item/<detail_id>', remove_cart_item),
    path('request/',send_request, name='request'),
    path('verify/<order_id>', verify, name='verify'),



]