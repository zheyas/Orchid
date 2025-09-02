from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.doctors_list, name='list'),
    path('specialization/<str:specialization_name>/', views.doctors_by_specialization, name='by_specialization'),
    path('<int:pk>/', views.doctor_detail, name='detail'),
]
