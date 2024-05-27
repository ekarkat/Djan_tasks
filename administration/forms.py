
from django.contrib.auth.password_validation import CommonPasswordValidator
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import UserProfile


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return confirm_password

    def save(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True,
        )
        instance = UserProfile.objects.create(
            user=user,
            email=email,
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            phone=self.cleaned_data.get('phone'),
            image=self.cleaned_data.get('image'),
        )
        return instance

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name', 'last_name', 'phone', 'image']


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=63, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
