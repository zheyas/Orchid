from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import RegistrationForm, ProfileUpdateForm


@login_required
def profile(request):
    """
    Личный кабинет пользователя: статистика, кнопки переходов.
    """
    stats = {
        "completed_appointments": 12,   # временные данные, потом заменишь на реальные запросы
        "analyses": 8,
        "upcoming": 2,
        "prescriptions": 3,
    }
    return render(request, "users/profile.html", {
        "stats": stats,
    })

@login_required
def logout_confirm(request):
    if request.method == "POST":
        # Пользователь подтвердил выход
        logout(request)
        return redirect('home')  # Перенаправление на главную страницу
    return render(request, "users/logout_confirm.html")

@login_required
def profile_edit(request):
    """
    Редактирование профиля пользователя.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Профиль обновлён успешно.')
            return redirect('users:profile')
        else:
            messages.error(request, '❌ Пожалуйста, исправьте ошибки в форме.')
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "users/profile_edit.html", {"form": form})


def register(request):
    """
    Регистрация нового пользователя.
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            authed = authenticate(
                request,
                username=(user.email or user.phone),
                password=raw_password
            )
            if authed is not None:
                login(request, authed)
            messages.success(request, '✅ Регистрация успешна! Добро пожаловать.')
            return redirect('users:profile')

        else:
            messages.error(request, '❌ Пожалуйста, исправьте ошибки в форме.')
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})

def profile_edit(request):
    pass