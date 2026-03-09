from rest_framework.permissions import BasePermission


class IsLibrarianOrOwner(BasePermission):
    """
    Разрешает действия:
    - Владельцу объекта (user == request.user)
    - Сотрудникам (is_librarian=True)
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_librarian


class IsLibrarian(BasePermission):
    """
    Доступ только для сотрудников (is_librarian=True).
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_librarian

    def has_object_permission(self, request, view, obj):
        return request.user.is_librarian
