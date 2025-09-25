"""
URL configuration for poushia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from poushia_products.views import products_categories_partial

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('',include('poushia_products.urls',namespace='products')),
    path('', include('poushia_order.urls', namespace='order')),
    path('', include('poushia_profile.urls', namespace='profile')),
    path('products_categories_partial', products_categories_partial, name='products_categories_partial'),
    path('wishlist/', include('wishlist.urls')),
    path('styleboard/', include('styleboard.urls')),
    path('discount/', include('discount.urls')),

]
