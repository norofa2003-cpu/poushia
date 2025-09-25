from django.contrib.auth import authenticate, login, get_user_model, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm
from poushia_sliders.models import Slider
from poushia_settings.models import Settings
from poushia_products.models import Product

def header(request):
    settings = Settings.objects.first()
    context = {
        'items2' : 'items2',
        'menu_item' :'منو سفارشی از رندر پارشیال',
        'settings' : settings,
    }
    return render(request, 'base/header.html', context)


def footer(request):
    settings = Settings.objects.first()
    context = {
        'settings': settings,
    }
    return render(request, 'base/footer.html', context)


def home_page(request):
    featured_products = Product.objects.filter(featured=True)
    most_visits_products = Product.objects.order_by('-visits').all()[:5]
    latest_products = Product.objects.order_by('-id').all()[:5]
    sliders = Slider.objects.all()
    context = {
        'sliders': sliders,
        'featured_products': featured_products,
        'most_visits_products': most_visits_products,
        'latest_products': latest_products,
    }
    return render(request, 'main/home_page.html', context)




# AUTH section
def login_page(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        userName = login_form.cleaned_data.get('userName')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=userName, password=password)
        if user is not None:
            login(request, user)
            return redirect('/profile')
        else:
            print('Error')

    context = {
        'login_form': login_form
    }
    return render(request, 'main/login.html', context)


User = get_user_model()


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    if register_form.is_valid():
        userName = register_form.cleaned_data.get('userName')
        email = register_form.cleaned_data.get('email')
        password = register_form.cleaned_data.get('password')
        new_user = User.objects.create_user(username=userName, email=email, password=password)
        print(new_user)
    context = {
        'register_form': register_form
    }
    return render(request, 'main/register.html', context)


def log_out(request):
    logout(request)
    return redirect('/login')

# AUTH section
