from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "avatar", "phone_number"]
        read_only_fields = ["is_librarian", "is_superuser"]
