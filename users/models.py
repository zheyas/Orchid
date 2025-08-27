# users/models.py
import re
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

PHONE_VALIDATOR = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message=_('Введите корректный телефон в формате +79991234567'),
)

def normalize_phone(phone: str | None) -> str | None:
    if not phone:
        return None
    digits = re.sub(r'\D+', '', phone)
    if not digits:
        return None
    # Простейшая нормализация для РФ
    if digits.startswith('8') and len(digits) == 11:
        digits = '7' + digits[1:]
    if digits.startswith('9') and len(digits) == 10:
        digits = '7' + digits
    if not digits.startswith('7') and not digits.startswith('1') and len(digits) >= 10:
        # fallback для иных стран: просто вернем в +<digits>
        return f'+{digits}'
    return f'+{digits}'

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phone, password, **extra_fields):
        if not email and not phone:
            raise ValueError('Нужно указать email или телефон')
        email = self.normalize_email(email) if email else None
        phone = normalize_phone(phone)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, phone, password, **extra_fields)

    def create_superuser(self, email=None, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if not password:
            raise ValueError('Пароль обязателен для суперпользователя')
        # если email не указан — используем заглушку
        return self._create_user(email or 'admin@example.com', phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(_('email'), unique=True, blank=True, null=True)
    phone = models.CharField(_('телефон'), max_length=16, unique=True, blank=True, null=True, validators=[PHONE_VALIDATOR])

    first_name = models.CharField(_('имя'), max_length=150, blank=True)
    last_name = models.CharField(_('фамилия'), max_length=150, blank=True)

    is_active = models.BooleanField(_('активен'), default=True)
    is_staff = models.BooleanField(_('персонал'), default=False)
    date_joined = models.DateTimeField(_('дата регистрации'), default=timezone.now)

    objects = UserManager()

    # Базовое поле для "логина" — email, а телефон обрабатываем в backend-е
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # можно добавить 'phone' по желанию

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)
        if self.phone:
            self.phone = normalize_phone(self.phone)
        super().save(*args, **kwargs)
