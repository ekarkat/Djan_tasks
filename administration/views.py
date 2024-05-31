from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

from .forms import RegisterForm, LoginForm

# Create your views here.
def register(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'administration/register_success.htm')

        return render(request, 'administration/register.htm', context={'form': form})

    form = RegisterForm()
    return render(request, 'administration/register.htm', context={'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user.username)
                login(request, user)
                return redirect('core:home')  # Redirect to a success page.
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'administration/login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('core:home')
