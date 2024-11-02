from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name="Аватар")
    phone_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=100, null=True, blank=True, verbose_name="Страна")
    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    username = models.CharField(max_length=50, unique=True, verbose_name="Имя пользователя")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
    ]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]
