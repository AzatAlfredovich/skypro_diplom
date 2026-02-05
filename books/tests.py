from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authors.models import Author
from books.models import Book, BookIssue
from users.models import User


class BookAPITest(APITestCase):
    def setUp(self):
        # Создаём пользователя‑библиотекаря и обычного пользователя
        self.librarian = User.objects.create(
            email="librarian@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="password123",
            phone_number="+79991234567",
            is_librarian=True,  # Важно для разрешений IsLibrarian
        )

        self.user = User.objects.create(
            email="test@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="password123",
            phone_number="+79991234567",
            is_librarian=False,
        )

        # Создаём тестового автора и книгу
        self.author = Author.objects.create(
            first_name="Лев",
            last_name="Толстой",
            birth_date="1828-09-09",
            biography="Великий русский писатель",
        )

        self.book = Book.objects.create(
            title="Война и мир",
            article="BK001",
            genre="Роман",
            publication_year=1869,
            pages=1225,
            description="Эпический роман",
            author=self.author,
            is_available=True,
        )

        # URLs
        self.list_url = reverse("books:book_list")
        self.create_url = reverse("books:book_create")
        self.detail_url = reverse("books:book_detail", kwargs={"pk": self.book.pk})
        self.update_url = reverse("books:book_update", kwargs={"pk": self.book.pk})
        self.delete_url = reverse("books:book_delete", kwargs={"pk": self.book.pk})

    def test_book_str(self):
        """Проверка строкового представления Book."""
        expected_str = "Книга: Война и мир, Автор: Лев Толстой"
        self.assertEqual(str(self.book), expected_str)

    def test_list_books_authenticated(self):
        """GET / — список книг (авторизованный доступ)."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Война и мир")

    def test_list_books_unauthenticated(self):
        """GET / — запрет без авторизации."""
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_success(self):
        """POST /create/ — успешное создание книги (библиотекарь)."""
        self.client.force_authenticate(user=self.librarian)
        data = {
            "title": "Анна Каренина",
            "article": "BK002",
            "genre": "Роман",
            "publication_year": 1877,
            "pages": 864,
            "description": "Роман о любви",
            "author": self.author.id,
            "is_available": True,
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data["title"], "Анна Каренина")

    def test_create_book_unauthorized(self):
        """POST /create/ — запрет для не‑библиотекаря."""
        self.client.force_authenticate(user=self.user)
        data = {"title": "Новая книга", "article": "BK003", "author": self.author.id}
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_book_success(self):
        """GET /<pk>/ — получение книги."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Война и мир")
        self.assertEqual(response.data["article"], "BK001")

    def test_update_book_success(self):
        """PUT /<pk>/update/ — обновление книги (библиотекарь)."""
        self.client.force_authenticate(user=self.librarian)
        data = {"title": "Война и Мир (исправл.)", "pages": 1300}
        response = self.client.patch(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Война и Мир (исправл.)")
        self.assertEqual(self.book.pages, 1300)

    def test_delete_book_success(self):
        """DELETE /<pk>/delete/ — удаление книги (библиотекарь)."""
        self.client.force_authenticate(user=self.librarian)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())


class BookIssueAPITest(APITestCase):
    def setUp(self):
        # Создаём пользователя‑библиотекаря и обычного пользователя
        self.librarian = User.objects.create(
            email="librarian@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="password123",
            phone_number="+79991234567",
            is_librarian=True,  # Важно для разрешений IsLibrarian
        )

        self.user = User.objects.create(
            email="test@example.com",
            first_name="Иван",
            last_name="Иванов",
            password="password123",
            phone_number="+79991234567",
            is_librarian=False,
        )

        # Создаём тестового автора и книгу
        self.author = Author.objects.create(
            first_name="Лев",
            last_name="Толстой",
            birth_date="1828-09-09",
            biography="Великий русский писатель",
        )

        self.book = Book.objects.create(
            title="Война и мир",
            article="BK001",
            genre="Роман",
            publication_year=1869,
            pages=1225,
            description="Эпический роман",
            author=self.author,
            is_available=True,
        )

        self.issue = BookIssue.objects.create(
            book=self.book, user=self.user, due_date="2025-12-31T00:00:00Z"
        )

        # URLs
        self.issues_list_url = reverse("books:issue_list")
        self.issue_create_url = reverse("books:issue_create")
        self.issue_detail_url = reverse(
            "books:issue_detail", kwargs={"pk": self.issue.pk}
        )
        self.issue_update_url = reverse(
            "books:issue_update", kwargs={"pk": self.issue.pk}
        )
        self.issue_delete_url = reverse(
            "books:issue_delete", kwargs={"pk": self.issue.pk}
        )

    def test_book_issue_str(self):
        """Проверка строкового представления BookIssue."""
        expected_str = "Взятая под запись книга: Война и мир, читатель: Иван Иванов"
        self.assertEqual(str(self.issue), expected_str)

    def test_list_issues_user(self):
        """GET /issues/ — список своих выдач (читатель)."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.issues_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_issues_librarian(self):
        """GET /issues/ — список всех выдач (библиотекарь)."""
        self.client.force_authenticate(user=self.librarian)
        response = self.client.get(self.issues_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_issue_success(self):
        self.client.force_authenticate(user=self.librarian)
        data = {
            "book": self.book.id,
            "user": self.user.id,
            "due_date": "2025-12-31T00:00:00Z",
        }
        response = self.client.post(self.issue_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(BookIssue.objects.count(), 2)

    def test_create_issue_book_not_available(self):
        self.client.force_authenticate(user=self.librarian)
        self.book.is_available = False
        self.book.save()
        data = {
            "book": self.book.id,
            "user": self.user.id,
            "due_date": "2025-12-31T00:00:00Z",
        }
        response = self.client.post(self.issue_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("book", response.data)

    def test_update_issue_mark_returned(self):
        self.client.force_authenticate(user=self.librarian)
        data = {"is_returned": True}
        response = self.client.patch(self.issue_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.issue.refresh_from_db()
        self.assertTrue(self.issue.is_returned)
        self.assertIsNotNone(self.issue.return_date)
        self.assertTrue(self.book.is_available)

    def test_update_issue_unauthorized(self):
        self.client.force_authenticate(user=self.user)
        data = {"is_returned": True}
        response = self.client.patch(self.issue_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_issue_success(self):
        self.client.force_authenticate(user=self.librarian)
        response = self.client.delete(self.issue_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BookIssue.objects.filter(pk=self.issue.pk).exists())

    def test_retrieve_issue_unauthorized(self):
        other_user = User.objects.create(
            email="testother@example.com",
            first_name="Сергей",
            last_name="Иванов",
            password="password123",
            phone_number="+79991234567",
            is_librarian=False,
        )

        other_issue = BookIssue.objects.create(
            book=self.book, user=other_user, due_date="2025-12-31T00:00:00Z"
        )
        url = reverse("books:issue_detail", kwargs={"pk": other_issue.pk})

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_issue_invalid_due_date(self):
        self.client.force_authenticate(user=self.librarian)
        data = {"book": self.book.id, "user": self.user.id, "due_date": "invalid-date"}
        response = self.client.post(self.issue_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("due_date", response.data)

    def test_permissions_book_list_for_anonymous(self):
        response = self.client.get(self.issues_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_issue_list_for_anonymous(self):
        response = self.client.get(self.issues_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_create_book_for_reader(self):
        self.client.force_authenticate(user=self.user)
        data = {"title": "Новая книга", "article": "BK006", "author": self.author.id}
        response = self.client.post(self.issue_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_permissions_update_issue_for_reader(self):
        self.client.force_authenticate(user=self.user)
        data = {"is_returned": True}
        response = self.client.patch(self.issue_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
