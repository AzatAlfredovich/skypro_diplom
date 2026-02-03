from django.contrib import admin

from books.models import Book, BookIssue


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "article",
        "author",
        "publication_year",
        "genre",
        "is_available",
    )
    list_filter = ("genre", "publication_year", "is_available", "author")
    search_fields = ("title", "article", "author__last_name", "author__first_name")
    ordering = ("id", "title")


@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "book",
        "user",
        "issue_date",
        "return_date",
        "due_date",
        "is_returned",
    )
    list_filter = (
        "is_returned",
        "issue_date",
        "due_date",
        "book__title",
        "user__last_name",
        "user__first_name",
    )
    search_fields = (
        "book__title",
        "user__first_name",
        "user__last_name",
        "user__email",
    )
    ordering = (
        "id",
        "-issue_date",
    )
