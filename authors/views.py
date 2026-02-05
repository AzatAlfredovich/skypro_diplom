from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated

from authors.models import Author
from authors.serializers import AuthorSerializer
from users.permissions import IsLibrarian


class AuthorListAPIView(ListAPIView):
    """
    GET: список всех авторов.
    Доступ: только библиотекари (is_staff=True).
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["first_name", "last_name"]


class AuthorCreateAPIView(CreateAPIView):
    """
    POST: создание нового автора.
    Доступ: только библиотекари (is_staff=True).
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]


class AuthorRetrieveAPIView(RetrieveAPIView):
    """
    GET: детальная информация об авторе.
    Доступ: только библиотекари (is_staff=True).
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]


class AuthorUpdateAPIView(UpdateAPIView):
    """
    PUT/PATCH: редактирование автора.
    Доступ: только библиотекари (is_staff=True).
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]


class AuthorDestroyAPIView(DestroyAPIView):
    """
    DELETE: удаление автора.
    Доступ: только библиотекари (is_staff=True).
    """

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsLibrarian]
