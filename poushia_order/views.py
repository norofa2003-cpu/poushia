import time
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from poushia_order.forms import UserNewOrderForm
from poushia_order.models import Order, OrderDetail
from poushia_products.models import Product, Color, Size

# zarin
from django.http import HttpResponse, Http404
import requests
import json

# Create your views here.
@login_required(login_url='/login')
def add_new_order(request):
    new_order_form = UserNewOrderForm(request.POST or None)
    if new_order_form.is_valid():
        order = Order.objects.filter(user_id=request.user.id, paid=False).first()
        if order is None:
            order = Order.objects.create(user_id=request.user.id, paid=False)

        product_id = new_order_form.cleaned_data.get('product_id')
        product = Product.objects.get_product_by_id(product_id)
        count = new_order_form.cleaned_data.get('count')
        if count < 0:
            count = 1

        # گرفتن رنگ و سایز از فرم
        selected_color = request.POST.get('color')
        selected_size = request.POST.get('size')

        order.orderdetail_set.create(
            product_id=product_id,
            count=count,
            price=product.price,
            selected_color_id=selected_color if selected_color else None,
            selected_size_id=selected_size if selected_size else None
        )

        return redirect(request.META.get('HTTP_REFERER','/'))


@login_required(login_url='/login')
def cart(request):
    context = {
        'order': None,
        'details': None,
        'total_price': 0,
        'original_price': 0,
        'discount_percent': 0
    }

    open_orders: Order = Order.objects.filter(user_id=request.user.id, paid=False).first()
    if open_orders is not None:
        original_price = open_orders.total_price()
        discount = request.session.get('discount_percent', 0)
        total_price = int(original_price * (100 - discount) / 100)

        context['order'] = open_orders
        context['details'] = open_orders.orderdetail_set.all()
        context['original_price'] = original_price
        context['discount_percent'] = discount
        context['total_price'] = total_price

    return render(request, 'cart_page.html', context)


@login_required(login_url='/login')
def remove_cart_item(request, *args, **kwargs):
    detail_id = kwargs['detail_id']
    order_detail = OrderDetail.objects.get_queryset().get(id=detail_id, order__user_id=request.user.id)
    if order_detail is not None:
        order_detail.delete()
        return redirect('/cart')
    raise Http404()


MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://localhost:8000/verify'


def send_request(request):
    open_orders: Order = Order.objects.filter(user_id=request.user.id, paid=False).first()
    if open_orders is not None:
        total_price = open_orders.total_price()
        print(total_price)
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "callback_url": f"{CallbackURL}/{open_orders.id}",
            "description": description,
            "metadata": {"mobile": mobile, "email": email}
        }
        req_header = {"accept": "application/json","content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
           return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
          e_code = req.json()['errors']['code']
          e_message = req.json()['errors']['message']
          return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


def verify(request, *args, **kwargs):
    order_id = kwargs['order_id']
    t_status = request.GET.get('Status')
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": amount,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                order = Order.objects.get_queryset().get(id=order_id)
                order.paid = True
                order.pay_date = time.time()
                order.save()
                context = {
                    'refID' : str(req.json()['data']['ref_id'])
                }
                return render(request, '',context)

            elif t_status == 101:
                return HttpResponse('Transaction submitted : ' + str(
                    req.json()['data']['message']
                ))
            else:
                return HttpResponse('Transaction failed.\nStatus: ' + str(
                    req.json()['data']['message']
                ))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
    else:
        return HttpResponse('Transaction failed or canceled by user')


