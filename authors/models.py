from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Дата рождения")
    biography = models.TextField(blank=True, verbose_name="Биография")

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"Автор: {self.first_name} {self.last_name}"
