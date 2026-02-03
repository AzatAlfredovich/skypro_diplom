from django.db import models

from authors.models import Author
from users.models import User


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название")
    article = models.CharField(max_length=15, unique=True, verbose_name="Артикул")
    genre = models.CharField(max_length=50, blank=True, verbose_name="Жанр")
    publication_year = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Год издания"
    )
    pages = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="Количество страниц"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name="book_authors",
        verbose_name="Автор",
    )

    # Статус наличия
    is_available = models.BooleanField(default=True, verbose_name="Доступна для выдачи")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"
        ordering = ["title"]

    def __str__(self):
        return f"Книга: {self.title}, автор: {self.author}"


class BookIssue(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="book_issues", verbose_name="Книга"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="taken_books_users",
        verbose_name="Пользователь",
    )
    issue_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи")
    return_date = models.DateTimeField(
        null=True, blank=True, verbose_name="Дата возврата"
    )
    is_returned = models.BooleanField(
        default=False, verbose_name="Возвращена ли книга?"
    )
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Срок возврата")

    class Meta:
        verbose_name = "Выдача книги"
        verbose_name_plural = "Выдачи книг"
        ordering = ["user"]

    def __str__(self):
        return f"Взятая под запись книга:{self.book.title}, читатель: {self.user.first_name} {self.user.last_name}"
