from django.http import Http404
from django.shortcuts import render
from django.views.generic.list import ListView
from unicodedata import category
from poushia_products_category.models import ProductCategory
from poushia_tag.models import Tag
from .models import Product, ProductGallery
from poushia_order.forms import UserNewOrderForm




# Create your views here.


class ProductsList(ListView):
    template_name = 'products_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Product.objects.get_active_products()


class ProductsListByCategory(ListView):
    template_name = 'products_list.html'
    paginate_by = 10

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        print(category_name)
        categories = ProductCategory.objects.filter(name__iexact=category_name)
        if categories is None:
            raise Http404('صفحه مورد نظر یافت نشد!')

        return Product.objects.get_product_by_category(category_name)


def products_categories_partial(request):
    categories = ProductCategory.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'categories_view_partial.html', context)


def product_detail(request, *args, **kwargs):
    get_product_id = kwargs['product_id']
    new_order_form = UserNewOrderForm(request.POST or None, initial={'product_id': get_product_id})

    product = Product.objects.get_product_by_id(get_product_id)
    if product is None:
        raise Http404('محصول مورد نظر یافت نشد!')

    product.visits += 10
    product.save()

    gallery = ProductGallery.objects.filter(product_id=get_product_id)

    related_products = Product.objects.get_queryset().filter(category__product=product).distinct()
    print(related_products)

    context = {
        'product': product,
        'gallery': gallery,
        'related_products': related_products,
        'new_order_form': new_order_form,
    }

    return render(request, 'product_detail.html', context)


class SearchProducts(ListView):
    template_name = 'products_list.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        if query is not None:
            return Product.objects.search_products(query)
        return Product.objects.get_active_products()
