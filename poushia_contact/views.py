from django.conf import settings
from django.shortcuts import render
from .models import ContactUs

from .forms import ContactUsForm
from poushia_settings.models import Settings
# Create your views here.


def contact_us_page(request):
    contact_form = ContactUsForm(request.POST or None)
    if contact_form.is_valid():
        full_name = contact_form.cleaned_data.get('full_name')
        email = contact_form.cleaned_data.get('email')
        message = contact_form.cleaned_data.get('message')
        new_contact = ContactUs.objects.create(full_name=full_name, email=email, message=message)
        print(new_contact)


    settings = Settings.objects.first()
    context ={
        'contact_form': contact_form,
        'settings': settings,
    }
    return render(request, 'contact_us_page.html',context )

