from django.db import IntegrityError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserModelTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="test@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="password123",
            phone_number="+79991234567",
            is_librarian=False,
        )

    def test_user_creation(self):
        """Проверка создания пользователя."""
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.first_name, "Иван")
        self.assertEqual(self.user.last_name, "Иванов")
        self.assertEqual(self.user.phone_number, "+79991234567")
        self.assertFalse(self.user.is_librarian)

    def test_str_method(self):
        """Метод __str__ возвращает email."""
        self.assertEqual(str(self.user), "test@example.com")

    def test_email_unique(self):
        """Поле email уникально."""
        with self.assertRaises(Exception):
            User.objects.create(email="test@example.com", password="123")

    def test_required_fields(self):
        """Обязательные поля: email, first_name, last_name."""
        # Без email
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email=None,
                first_name="Алексей",
                last_name="Петров",
                password="password123",
            )


class UserAPITest(APITestCase):
    def setUp(self):
        # Создаём пользователей
        self.librarian = User.objects.create(
            email="librarian@test.com", password="pass123", is_librarian=True
        )
        self.owner = User.objects.create(email="owner@test.com", password="pass123")
        self.other_user = User.objects.create(
            email="other@test.com", password="pass123"
        )

        # URL
        self.register_url = reverse("users:register")
        self.list_url = reverse("users:users_list")
        self.retrieve_url = reverse("users:user_retrieve", kwargs={"pk": self.owner.pk})
        self.update_url = reverse("users:user_update", kwargs={"pk": self.owner.pk})
        self.delete_url = reverse("users:user_delete", kwargs={"pk": self.owner.pk})

    def test_register_user_success(self):
        """Успешная регистрация."""
        data = {
            "email": "new@test.com",
            "password": "securepass123",
            "first_name": "Алексей",
            "last_name": "Сидоров",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email="new@test.com")
        self.assertEqual(user.first_name, "Алексей")
        self.assertEqual(user.last_name, "Сидоров")
        self.assertTrue(user.is_active)

    def test_register_missing_required_fields(self):
        """Ошибка при отсутствии обязательных полей."""
        data = {"email": "incomplete@test.com"}  # Нет first_name/last_name
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_users_librarian(self):
        """Библиотекарь видит всех активных пользователей."""
        self.client.force_authenticate(user=self.librarian)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_users_owner(self):
        """Владелец не видит список пользователей."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_owner(self):
        """Владелец получает свои данные."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.owner.email)

    def test_retrieve_librarian(self):
        """Библиотекарь получает чужие данные."""
        self.client.force_authenticate(user=self.librarian)
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_other_user_forbidden(self):
        """Другой пользователь не может получить чужие данные."""
        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(self.retrieve_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_owner(self):
        """Владелец обновляет свои данные."""
        self.client.force_authenticate(user=self.owner)
        data = {"phone_number": "+79997778899"}
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.owner.refresh_from_db()
        self.assertEqual(self.owner.phone_number, "+79997778899")

    def test_update_librarian(self):
        """Библиотекарь обновляет чужие данные."""
        self.client.force_authenticate(user=self.librarian)
        data = {"phone_number": "+79997778899"}
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_owner_forbidden(self):
        """Владелец не может удалить себя."""
        self.client.force_authenticate(user=self.owner)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_librarian_success(self):
        """Библиотекарь удаляет пользователя."""
        self.client.force_authenticate(user=self.librarian)
