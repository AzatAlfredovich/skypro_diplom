from django.urls import path

from authors.apps import AuthorsConfig
from authors.views import (
    AuthorCreateAPIView,
    AuthorDestroyAPIView,
    AuthorListAPIView,
    AuthorRetrieveAPIView,
    AuthorUpdateAPIView,
)

app_name = AuthorsConfig.name

urlpatterns = [
    path("", AuthorListAPIView.as_view(), name="author-list"),
    path("create/", AuthorCreateAPIView.as_view(), name="author-create"),
    path("<int:pk>/", AuthorRetrieveAPIView.as_view(), name="author-detail"),
    path("<int:pk>/update/", AuthorUpdateAPIView.as_view(), name="author-update"),
    path("<int:pk>/delete/", AuthorDestroyAPIView.as_view(), name="author-delete"),
]
