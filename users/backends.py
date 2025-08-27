# users/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import normalize_phone

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        if not username or not password:
            return None
        login = username.strip()
        user = None
        # Сначала ищем по email (без учета регистра)
        try:
            user = User.objects.get(email__iexact=login)
        except User.DoesNotExist:
            # Пробуем как телефон
            phone = normalize_phone(login)
            if phone:
                try:
                    user = User.objects.get(phone=phone)
                except User.DoesNotExist:
                    user = None
        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None