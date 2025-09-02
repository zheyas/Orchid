# doctors/utils.py
from .models import Doctor

SPECIALIZATION_MAP = {
    'Терапия': 'Терапевт',
    'Кардиология': 'Кардиолог',
    'Неврология': 'Невролог',
    'Психология': 'Психолог',
    'Лабораторная диагностика': [
        'Лаборант-исследователь',
        'Медицинская сестра',
        'Медбрат',
        'Врач/специалист Лабораторной диагностики'
    ]
}

def get_doctors_by_qualification(qualification: str = None):
    """
    Возвращает список активных врачей.
    Если передана qualification, фильтрует по профессии.
    Для 'Лабораторная диагностика' вычисляет медсестру/медбрата по полу.
    """
    doctors = Doctor.objects.filter(is_active=True)

    if qualification:
        if qualification.lower() == 'лабораторная диагностика':
            doctors = doctors.filter(qualification__in=SPECIALIZATION_MAP['Лабораторная диагностика'])
        else:
            doctors = doctors.filter(qualification__iexact=qualification)

    doctors = doctors.order_by('last_name')
    doctors_list = list(doctors)

    # Устанавливаем display_qualification
    for doctor in doctors_list:
        if qualification and qualification.lower() == 'лабораторная диагностика':
            doctor.display_qualification = doctor.get_gendered_title()
        elif qualification in SPECIALIZATION_MAP:
            doctor.display_qualification = qualification  # <--- только название специализации
        else:
            doctor.display_qualification = doctor.qualification

    return doctors_list
