from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.models import Author
from users.models import User


class AuthorAPITest(APITestCase):
    def setUp(self):
        # Создаём пользователя‑библиотекаря (требуется для доступа)
        self.librarian = User.objects.create(
            email="librarian@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="password123",
            phone_number="+79991234567",
            is_librarian=True,  # Важно для разрешений IsLibrarian
        )

        # Авторизуемся как библиотекарь
        self.client.force_authenticate(user=self.librarian)

        # Создаём тестового автора
        self.author = Author.objects.create(
            first_name="Лев",
            last_name="Толстой",
            birth_date="1828-09-09",
            biography="Великий русский писатель",
        )

        # URLs
        self.list_url = reverse("authors:author_list")
        self.create_url = reverse("authors:author_create")
        self.detail_url = reverse(
            "authors:author_detail", kwargs={"pk": self.author.pk}
        )
        self.update_url = reverse(
            "authors:author_update", kwargs={"pk": self.author.pk}
        )
        self.delete_url = reverse(
            "authors:author_delete", kwargs={"pk": self.author.pk}
        )

    def test_author_str(self):
        """Проверка строкового представления Author"""
        expected_str = "Автор: Лев Толстой"
        self.assertEqual(str(self.author), expected_str)

    def test_list_authors_authenticated(self):
        """GET / — список авторов (авторизованный доступ)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["first_name"], "Лев")
        self.assertEqual(response.data[0]["last_name"], "Толстой")

    def test_list_authors_unauthenticated(self):
        """GET / — запрет без авторизации."""
        self.client.force_authenticate(user=None)  # Снимаем авторизацию
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_author_success(self):
        """POST /create/ — успешное создание автора."""
        data = {
            "first_name": "Антон",
            "last_name": "Чехов",
            "birth_date": "1860-01-29",
            "biography": "Русский писатель и драматург",
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Author.objects.count(), 2)
        self.assertEqual(response.data["first_name"], "Антон")
        self.assertEqual(response.data["last_name"], "Чехов")

    def test_create_author_missing_fields(self):
        """POST /create/ — ошибка при отсутствии обязательных полей."""
        data = {"first_name": ""}  # Пустое имя
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)  # Поле обязано быть заполнено

    def test_retrieve_author_success(self):
        """GET /<pk>/ — получение автора."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Лев")
        self.assertEqual(response.data["last_name"], "Толстой")
        self.assertIn("birth_date", response.data)
        self.assertIn("biography", response.data)

    def test_retrieve_author_not_found(self):
        """GET /<pk>/ — автор не найден."""
        url = reverse("authors:author_detail", kwargs={"pk": 999})  # Неверный ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_author_full(self):
        """PUT /<pk>/update/ — полное обновление автора."""
        data = {
            "first_name": "Лев Николаевич",
            "last_name": "Толстой",
            "birth_date": "1828-09-09",
            "biography": "Обновлённая биография",
        }
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.first_name, "Лев Николаевич")
        self.assertEqual(self.author.biography, "Обновлённая биография")

    def test_update_author_partial(self):
        """PATCH /<pk>/update/ — частичное обновление."""
        data = {"biography": "Частично обновлённая биография"}
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.author.refresh_from_db()
        self.assertEqual(self.author.biography, "Частично обновлённая биография")

    def test_update_author_invalid_data(self):
        """PUT /<pk>/update/ — ошибка валидации (некорректная дата)."""
        data = {"birth_date": "invalid-date"}
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("birth_date", response.data)

    def test_delete_author_success(self):
        """DELETE /<pk>/delete/ — удаление автора."""
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(pk=self.author.pk).exists())

    def test_delete_author_not_found(self):
        """DELETE /<pk>/delete/ — автор не найден."""
        url = reverse("authors:author_delete", kwargs={"pk": 999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_permissions_for_non_librarian(self):
        """Проверка разрешений: обычный пользователь не может создавать/обновлять/удалять."""
        # Создаём обычного пользователя (не библиотекарь)
        user = User.objects.create(
            email="test@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="password123",
            phone_number="+79991234567",
            is_librarian=False,
        )
        self.client.force_authenticate(user=user)

        # POST /create/
        data = {"first_name": "Иван", "last_name": "Иванов"}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # PUT /update/
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # DELETE /delete/
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
