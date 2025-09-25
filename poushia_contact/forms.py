from django import forms


class ContactUsForm(forms.Form):
    full_name = forms.CharField(
        label="نام",
        widget=forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
    )
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label="پیام",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )