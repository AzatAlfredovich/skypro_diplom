from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_librarian",
        "is_active",
    )
    list_filter = ("email", "last_name")
    search_fields = ("email", "last_name")
    ordering = ("id", "is_active")
