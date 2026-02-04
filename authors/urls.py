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
    path("", AuthorListAPIView.as_view(), name="author_list"),
    path("create/", AuthorCreateAPIView.as_view(), name="author_create"),
    path("<int:pk>/", AuthorRetrieveAPIView.as_view(), name="author_detail"),
    path("<int:pk>/update/", AuthorUpdateAPIView.as_view(), name="author_update"),
    path("<int:pk>/delete/", AuthorDestroyAPIView.as_view(), name="author_delete"),
]
