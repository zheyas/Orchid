# users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            authed = authenticate(request, username=(user.email or user.phone), password=raw_password)
            if authed is not None:
                login(request, authed)
            messages.success(request, '✅ Регистрация успешна! Добро пожаловать.')
            return redirect('home')
        else:
            messages.error(request, '❌ Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})
