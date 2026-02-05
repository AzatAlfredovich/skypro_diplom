from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from books.models import Book, BookIssue
from books.serializers import BookIssueSerializer, BookSerializer
from users.permissions import IsLibrarian


class BookListAPIView(ListAPIView):
    """
    GET: список всех книг.
    Доступ: любые авторизованные пользователи (IsAuthenticated).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "article", "genre", "author", "is_available"]


class BookCreateAPIView(CreateAPIView):
    """
    POST: создание новой книги.
    Доступ: только библиотекари (is_staff=True).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]


class BookRetrieveAPIView(RetrieveAPIView):
    """
    GET: детальная информация о книге.
    Доступ: любые авторизованные пользователи (IsAuthenticated).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateAPIView(UpdateAPIView):
    """
    PUT/PATCH: редактирование книги.
    Доступ: только библиотекари (is_staff=True).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]


class BookDestroyAPIView(DestroyAPIView):
    """
    DELETE: удаление книги.
    Доступ: только библиотекари (is_staff=True).
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsLibrarian]


# Выдача книг
class BookIssueListAPIView(ListAPIView):
    """
    GET: список выдач.
    - Пользователь: только свои выдачи.
    - Библиотекарь: все выдачи.
    Доступ: IsAuthenticated.
    """

    serializer_class = BookIssueSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_librarian:
            return BookIssue.objects.all()
        return BookIssue.objects.filter(user=self.request.user)


class BookIssueCreateAPIView(CreateAPIView):
    """
    POST: создание новой выдачи (только библиотекари).
    """

    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsLibrarian]

    def perform_create(self, serializer):
        book = serializer.validated_data["book"]

        # Проверка: доступна ли книга?
        if not book.is_available:
            raise ValidationError(
                {"book": "Эта книга уже выдана и недоступна для новой выдачи."}
            )

        # Если книга доступна — сохраняем выдачу
        serializer.save()


class BookIssueRetrieveAPIView(RetrieveAPIView):
    """
    GET: детальная информация о выдаче.
    - Пользователь: только если это его выдача.
    - Библиотекарь: любая выдача.
    """

    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_librarian and obj.user != self.request.user:
            raise PermissionDenied("Вы не можете просматривать эту выдачу.")
        return obj


class BookIssueUpdateAPIView(UpdateAPIView):
    """
    PUT/PATCH: редактирование выдачи (только библиотекари).
    """

    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsLibrarian]

    def perform_update(self, serializer):
        instance = serializer.save()  # Сохраняем изменения (например, is_returned=True)

        # Если книга отмечена как возвращённая и return_date ещё не установлен
        if instance.is_returned and not instance.return_date:
            instance.return_date = timezone.now()  # Фиксируем дату возврата

        # Синхронизируем is_available книги с is_returned выдачи
        if instance.is_returned:
            instance.book.is_available = True  # Книга теперь доступна
        else:
            instance.book.is_available = False  # Книга снова выдана

        # Сохраняем изменения в книге
        instance.book.save()
        # Сохраняем изменения в выдаче (если менялись return_date)
        instance.save()


class BookIssueDestroyAPIView(DestroyAPIView):
    """
    DELETE: удаление выдачи (только библиотекари).
    """

    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
    permission_classes = [IsLibrarian]
