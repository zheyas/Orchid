#users/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import normalize_phone

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Email')
    phone = forms.CharField(required=False, label='Телефон', help_text='Например: +7XXXXXXXXXX')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_cls = 'w-full px-4 py-3 rounded-xl bg-white/80 focus:ring-2 focus:ring-indigo-400 outline-none'
        placeholders = {
            'email': 'name@example.com',
            'phone': '+7XXXXXXXXXX',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'password1': '••••••••',
            'password2': '••••••••',
        }
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', base_cls)
            if name in placeholders:
                field.widget.attrs.setdefault('placeholder', placeholders[name])

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email') or None
        phone_raw = cleaned.get('phone') or None

        norm_phone = None
        if phone_raw:
            norm_phone = normalize_phone(phone_raw)
            if not norm_phone:
                self.add_error('phone', 'Некорректный номер телефона.')

        if not email and not norm_phone:
            raise forms.ValidationError('Укажите телефон или email.')

        if email and User.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'Пользователь с таким email уже зарегистрирован.')

        if norm_phone and User.objects.filter(phone=norm_phone).exists():
            self.add_error('phone', 'Пользователь с таким телефоном уже зарегистрирован.')

        cleaned['email'] = email
        cleaned['phone'] = norm_phone
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.phone = self.cleaned_data.get('phone')
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base = 'w-full px-4 py-3 rounded-xl bg-white/80 focus:ring-2 focus:ring-indigo-400 outline-none'
        self.fields['username'].widget.attrs.setdefault('class', base)
        self.fields['username'].widget.attrs.setdefault('placeholder', 'Телефон или email')
        self.fields['password'].widget.attrs.setdefault('class', base)
        self.fields['password'].widget.attrs.setdefault('placeholder', 'Введите пароль')

class EmailOrPhoneAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Телефон или Email',
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Телефон или Email'})
    )

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон'}),
        }

    def clean_phone(self):
        phone_raw = self.cleaned_data.get('phone')
        from .models import normalize_phone
        phone = normalize_phone(phone_raw)
        if phone and User.objects.exclude(pk=self.instance.pk).filter(phone=phone).exists():
            raise forms.ValidationError('Пользователь с таким телефоном уже существует.')
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует.')
        return email
