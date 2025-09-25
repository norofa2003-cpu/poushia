from django.urls import path
from .views import ProductsList,product_detail,SearchProducts,ProductsListByCategory

app_name = 'poushia_products'

urlpatterns = [

    path('products', ProductsList.as_view(), name='products_list'),
    path('products/<product_id>/<title>',product_detail, name='product_detail'),
    path('products/search', SearchProducts.as_view()),
    path('products/<category_name>', ProductsListByCategory.as_view()),

]