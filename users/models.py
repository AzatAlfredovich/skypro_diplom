from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта")
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар"
    )
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )
    is_librarian = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
