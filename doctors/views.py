from django.shortcuts import render, get_object_or_404
from .models import Doctor
from .utils import get_doctors_by_qualification, SPECIALIZATION_MAP  # если хочешь использовать utils

def doctors_by_specialization(request, specialization_name: str):
    qualification = SPECIALIZATION_MAP.get(specialization_name, specialization_name)

    # если это список профессий (Лаборанты и др.), фильтруем по __in
    if isinstance(qualification, list):
        doctors = Doctor.objects.filter(is_active=True, qualification__in=qualification).order_by('last_name')
    else:
        doctors = get_doctors_by_qualification(qualification=qualification)

    return render(request, 'doctors/doctors_list.html', {
        'doctors': doctors,
        'specialization': specialization_name
    })
def doctors_list(request):
    doctors = Doctor.objects.filter(is_active=True).order_by('last_name')
    return render(request, 'doctors/doctors_list.html', {'doctors': doctors})

def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, is_active=True)
    return render(request, 'doctors/doctor_detail.html', {'doctor': doctor})
