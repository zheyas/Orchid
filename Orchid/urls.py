# 5) Orchid/urls.py — роут на главную, рендер home.html
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('users.urls', namespace='users')),  # <- добавили
    path('doctors/', include('doctors.urls', namespace='doctors')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)