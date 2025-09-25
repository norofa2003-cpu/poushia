from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from .forms import UserEditProfileForm
from django.contrib.auth.models import User
from poushia_order.models import Order


# Create your views here.

@login_required(login_url='login')
def profile_main_page(request):
    context = {}
    return render(request, 'profile_main_page.html', context)

@login_required(login_url='login')
def profile_user_order(request):
    orders = Order.objects.filter(user=request.user).order_by('-pay_date')
    context = {
        'orders': orders
    }
    return render(request, 'profile_user_orders.html', context,)


@login_required(login_url='login')
def profile_setting(request):
    user_id = request.user.id
    user = User.objects.get(id=user_id)
    if user is None:
        raise Http404()

    edit_form = UserEditProfileForm(request.POST or None, initial={'first_name': user.first_name, 'last_name': user.last_name})
    if edit_form.is_valid():
        first_name = edit_form.cleaned_data.get('first_name')
        last_name = edit_form.cleaned_data.get('last_name')
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    context = {
        'edit_form': edit_form,
    }
    return render(request, 'profile_setting.html', context)


@login_required(login_url='login')
def profile_sidebar(request):
    context = {}
    return render(request, 'profile_sidebar.html', context)
