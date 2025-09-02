from django.urls import path
from . import views
from .forms import LoginForm
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        authentication_form=LoginForm
    ), name='login'),
    path('logout/', views.logout_confirm, name='logout_confirm'),  # <-- теперь кастомная страница
    path('profile/', views.profile, name='profile'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
]
