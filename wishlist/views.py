from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Wishlist
from poushia_products.models import Product


@login_required(login_url='/login')
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/wishlist.html', {'items': items})



@login_required(login_url='/login')
def wishlist_list(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist/list.html', {'wishlist_items': wishlist_items})

@login_required(login_url='/login')
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect(request.META.get('HTTP_REFERER','/'))

@login_required(login_url='/login')
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist:list')