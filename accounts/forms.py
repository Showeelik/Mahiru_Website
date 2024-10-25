import json
import mimetypes
import re
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.core.validators import FileExtensionValidator

from .models import User


class RegisterForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False, help_text="Необязательное поле")
    country = forms.CharField(max_length=100, required=False, help_text="Необязательное поле")
    username = forms.CharField(max_length=50)    
    
    class Meta:
        model = User
        fields = ["username", "email"]
        
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Пользователь с таким именем уже существует")
        elif len(username) < 4:
            raise forms.ValidationError("Имя пользователя должно содержать не менее 4 символов")
        elif len(username) > 150:
            raise forms.ValidationError("Имя пользователя должно содержать не более 150 символов")
        with open("black_list_words.json", "r", encoding="utf-8") as f:
            words = json.load(f)
        for word in words:
            if word in username.lower().split():
                raise forms.ValidationError(f"Недопустимое слово: {word}")
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен содержать не менее 8 символов")
        return password
    
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"
        
        # Настраиваем атрибуты для конкретных полей
        custom_attrs = {
            "email": {
                "label": "Email",
                "placeholder": "Введите email",
                "type": "email",
            },
            "username": {
                "label": "Имя пользователя",
                "placeholder": "Введите имя пользователя",
                "type": "username",
            },
            "password": {
                "label": "Пароль",
                "type": "password",
                "placeholder": "Введите пароль",
            },
            "phone_number": {
                "label": "Номер телефона",
                "type": "tel",
                "placeholder": "Введите номер телефона",
            },
            "country": {
                "label": "Страна",
                "placeholder": "Введите страну",
            }
        }

        # Применяем кастомные атрибуты для каждого поля
        for field_name, attrs in custom_attrs.items():
            if field_name in self.fields:
                for attr, value in attrs.items():
                    if attr == "label":
                        self.fields[field_name].label = value
                    else:
                        self.fields[field_name].widget.attrs[attr] = value

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["email", "password"]

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        
        if email and password:
            if not User.objects.filter(email=email).exists():
                raise forms.ValidationError("Неверное имя пользователя или пароль")
            self.user_cache = User.objects.get(email=email)
            if not self.user_cache.check_password(password):
                raise forms.ValidationError("Неверное имя пользователя или пароль")
        return self.cleaned_data
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"

        # Настраиваем атрибуты для конкретных полей
        custom_attrs = {
            "username": {
                "label": "Email",
                "placeholder": "Введите email",
                "type": "email",
            },
            "password": {
                "label": "Пароль",
                "placeholder": "Введите пароль",
                "type": "password",
            }
        }

        # Применяем кастомные атрибуты для каждого поля
        for field_name, attrs in custom_attrs.items():
            if field_name in self.fields:
                for attr, value in attrs.items():
                    if attr == "label":
                        self.fields[field_name].label = value
                    else:
                        self.fields[field_name].widget.attrs[attr] = value
                
    
class ProfileForm(forms.ModelForm):
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
    ALLOWED_MIME_TYPES = ["image/jpeg", "image/png"]
    
    # Загружаем запрещенные слова один раз при загрузке формы
    with open("black_list_words.json", "r", encoding="utf-8") as f:
        BLACKLIST_WORDS = set(json.load(f))  # Используем множество для быстрого поиска
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "avatar", "phone_number", "country"]
        
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # Устанавливаем общие атрибуты для всех полей
        for field_name, field in self.fields.items():
            field.required = False
            field.widget.attrs["class"] = "form-control"
            if self.errors.get(field_name):
                field.widget.attrs["class"] += " is-invalid"

        # Настраиваем атрибуты для конкретных полей
        custom_attrs = {
            "username": {
                "label": "Имя пользователя",
                "placeholder": "Введите имя пользователя",
                "type": "username",
            },
            "email": {
                "label": "Email",
                "placeholder": "Введите email",
                "type": "email",
            },
            "phone_number": {
                "label": "Номер телефона",
                "placeholder": "Введите номер телефона",
                "type": "tel",
            },
            "country": {
                "label": "Страна",
                "placeholder": "Введите страну",
            },
            "avatar": {
                "type": "file",
            },
            "first_name": {
                "placeholder": "Введите имя",
            },
            "last_name": {
                "placeholder": "Введите фамилию",
            }
        }

        # Применяем кастомные атрибуты для каждого поля
        for field_name, attrs in custom_attrs.items():
            if field_name in self.fields:
                for attr, value in attrs.items():
                    if attr == "label":
                        self.fields[field_name].label = value
                    else:
                        self.fields[field_name].widget.attrs[attr] = value
                
        


    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")

        # Если номер телефона не указан, возвращаем его как есть
        if not phone_number:
            return phone_number

        # Проверка, чтобы номер содержал только допустимые символы (цифры и, возможно, '+')
        if not re.fullmatch(r'^\+?\d+$', phone_number):
            raise forms.ValidationError("Номер телефона должен содержать только цифры и может начинаться с '+' для международного формата.")

        # Проверка длины номера телефона
        if len(phone_number) < 10 or len(phone_number) > 15:
            raise forms.ValidationError("Номер телефона должен содержать от 10 до 15 цифр.")

        return phone_number
    
    def clean_country(self):
        country = self.cleaned_data.get("country")
        
        # Если поле пустое, просто возвращаем его
        if not country:
            return country
        
        # Преобразуем страну в lowercase и разбиваем на слова
        country_words = set(country.lower().split())
        
        # Проверяем пересечение слов в стране и в черном списке
        invalid_words = country_words & self.BLACKLIST_WORDS
        if invalid_words:
            raise forms.ValidationError(
                f"Недопустимые слова: {', '.join(invalid_words)}"
            )
        
        return country
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        
        # Если файла нет, просто возвращаем None
        if not avatar:
            return avatar

        # Проверка допустимых MIME-типов
        mime_type, _ = mimetypes.guess_type(avatar.name)
        if mime_type not in self.ALLOWED_MIME_TYPES:
            raise forms.ValidationError("Недопустимый тип файла. Пожалуйста, загрузите файл JPG или PNG.")

        # Проверка размера файла
        if avatar.size > self.MAX_FILE_SIZE:
            raise forms.ValidationError(f"Размер файла должен быть меньше {self.MAX_FILE_SIZE / (1024 * 1024):.1f} МБ.")

        return avatar
    

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
