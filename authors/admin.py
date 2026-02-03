from django.contrib import admin

from authors.models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "birth_date")
    list_filter = ("birth_date",)
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name")
