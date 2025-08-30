from django.shortcuts import render, get_object_or_404
from .models import Doctor

def doctors_list(request):
    doctors = Doctor.objects.filter(is_active=True).order_by('last_name')
    return render(request, 'doctors/doctors_list.html', {'doctors': doctors})

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})
