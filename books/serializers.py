from rest_framework import serializers

from books.models import Book, BookIssue


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "article",
            "genre",
            "publication_year",
            "pages",
            "description",
            "author",
            "is_available",
        ]
        read_only_fields = ["article"]


class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = [
            "id",
            "book",
            "user",
            "issue_date",
            "return_date",
            "is_returned",
            "due_date",
        ]
        read_only_fields = ["issue_date"]
