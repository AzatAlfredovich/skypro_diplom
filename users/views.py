from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import AllowAny

from users.models import User
from users.permissions import IsLibrarianOrOwner
from users.serializers import UserSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [IsLibrarianOrOwner]  # Только сотрудники и владельцы


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsLibrarianOrOwner]
    queryset = User.objects.all()  # Включаем неактивных

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsLibrarianOrOwner]
    queryset = User.objects.all()  # Включаем неактивных

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class UserDestroyAPIView(DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsLibrarianOrOwner]
    queryset = User.objects.all()

    def get_object(self):
        obj = super().get_object()
        if not obj.is_active:
            raise NotFound("Пользователь не найден или неактивен!")
        self.check_object_permissions(self.request, obj)
        return obj
