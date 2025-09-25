from django import forms
from django.contrib.auth import get_user_model
from django.core import validators


class LoginForm(forms.Form):
    userName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter your passowrd'})
    )

User = get_user_model()


class RegisterForm(forms.Form):
    userName = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'enter your username'}),
        validators=[
            validators.MaxLengthValidator(limit_value=20, message='نام کاربری نباید بیش از 20 کاراکتر باشد.')
        ]
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'enter your email'}),
        validators = [
        validators.EmailValidator('ایمیل نامعتبر است!')
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'enter your password'})
    )

    password2 = forms.CharField(
        label='Confirm password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 're-enter your password'})
    )

    def clean_userName(self):
        userName = self.cleaned_data.get('userName')
        query = User.objects.filter(username=userName)
        if query.exists():
            raise forms.ValidationError('Username is not available')
        return userName

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not "gmail.com" in email:
            raise forms.ValidationError('email has to be gmail.com')
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords don't match")

        return data
