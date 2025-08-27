# 5) Orchid/urls.py — роут на главную, рендер home.html
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('users.urls', namespace='users')),  # <- добавили
]
