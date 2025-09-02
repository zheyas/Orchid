from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# Можно определить какие-нибудь квалификации как отдельную модель (если нужно справочник)
class Qualification(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name='Название квалификации')

    def __str__(self):
        return self.name

class Doctor(models.Model):
    class Gender(models.TextChoices):
        MALE = 'M', _('Мужской')
        FEMALE = 'F', _('Женский')
        OTHER = 'O', _('Другой/не указан')

    first_name = models.CharField(_('Имя'), max_length=150)
    last_name = models.CharField(_('Фамилия'), max_length=150)
    patronymic = models.CharField(_('Отчество'), max_length=150, blank=True, null=True)
    birth_date = models.DateField(_('Дата рождения'), blank=True, null=True)
    email = models.EmailField(_('E-mail'), blank=True, null=True)
    phone = models.CharField(_('Телефон'), max_length=16, blank=True, null=True)

    photo = models.ImageField(_('Фотография'), upload_to='doctors/photos/', blank=True, null=True)
    qualification = models.CharField(_('Квалификация'), max_length=255)
    experience_years = models.PositiveIntegerField(_('Стаж (лет)'), default=0)
    education = models.CharField(_('Образование'), max_length=255, blank=True, null=True)
    place_of_work = models.CharField(_('Место работы'), max_length=255, blank=True, null=True)
    position = models.CharField(_('Должность'), max_length=255, blank=True, null=True)
    specializations = models.CharField(_('Специализации'), max_length=255, blank=True, null=True)
    certificates = models.TextField(_('Сертификаты, лицензии'), blank=True, null=True)
    bio = models.TextField(_('Биография, информация о себе'), blank=True, null=True)
    achievements = models.TextField(_('Достижения'), blank=True, null=True)
    consultation_price = models.DecimalField(_('Стоимость консультации'), max_digits=10, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(_('Активен'), default=True)
    gender = models.CharField(_('Пол'), max_length=1, choices=Gender.choices, default=Gender.OTHER)

    created_at = models.DateTimeField(_('Время создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Время обновления'), auto_now=True)

    class Meta:
        verbose_name = 'Врач'
        verbose_name_plural = 'Врачи'

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.qualification})'

    def get_gendered_title(self):
        """Возвращает корректное название медработника по полу для Лабораторной диагностики"""
        if self.qualification.lower() in ['мед.сестра', 'медбрат', 'лаборант-исследователь', 'врач/специалист лабораторной диагностики']:
            if self.gender == self.Gender.FEMALE:
                return "Мед.сестра"
            elif self.gender == self.Gender.MALE:
                return "Медбрат"
            else:
                return "Медицинский специалист"
        return self.qualification
