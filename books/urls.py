from django.urls import path

from books.apps import BooksConfig
from books.views import (
    BookCreateAPIView,
    BookDestroyAPIView,
    BookIssueCreateAPIView,
    BookIssueDestroyAPIView,
    BookIssueListAPIView,
    BookIssueRetrieveAPIView,
    BookIssueUpdateAPIView,
    BookListAPIView,
    BookRetrieveAPIView,
    BookUpdateAPIView,
)

app_name = BooksConfig.name

urlpatterns = [
    # Список книг
    path("", BookListAPIView.as_view(), name="book_list"),
    path("create/", BookCreateAPIView.as_view(), name="book_create"),
    path("<int:pk>/", BookRetrieveAPIView.as_view(), name="book_detail"),
    path("<int:pk>/update/", BookUpdateAPIView.as_view(), name="book_update"),
    path("<int:pk>/delete/", BookDestroyAPIView.as_view(), name="book_delete"),
    # Записи по выдаче книг
    path("issues/", BookIssueListAPIView.as_view(), name="issue_list"),
    path("issues/create/", BookIssueCreateAPIView.as_view(), name="issue_create"),
    path("issues/<int:pk>/", BookIssueRetrieveAPIView.as_view(), name="issue_detail"),
    path(
        "issues/<int:pk>/update/", BookIssueUpdateAPIView.as_view(), name="issue_update"
    ),
    path(
        "issues/<int:pk>/delete/",
        BookIssueDestroyAPIView.as_view(),
        name="issue_delete",
    ),
]
