from webbrowser import register

from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static
from .views import home_page, header, footer ,login_page,register_page,log_out
from poushia_contact.views import contact_us_page

urlpatterns = [
    path('', home_page, name='home'),
    path('header', header, name='header'),
    path('footer', footer, name='footer'),
    path('contact-us', contact_us_page, name='contact'),
    path('login', login_page, name='login'),
    path('register', register_page, name='register'),
    path('logout', log_out, name='logout'),

]

if settings.DEBUG :
  urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
  urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
