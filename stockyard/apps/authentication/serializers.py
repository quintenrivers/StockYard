from typing import List, Dict
from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializes registration requests and creates a new user
    """

    password: serializers.CharField = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token: serializers.CharField = serializers.CharField(
        max_length=255,
        read_only=True
    )

    class Meta:
        model: User = User

        # List of all fields that could be in a req or res
        fields: List[str] = [
            'email',
            'username',
            'password',
            'token',
        ]

    def create(self, validated_data) -> User:
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email: serializers.CharField = serializers.CharField(max_length=255)
    username: serializers.CharField = serializers.CharField(
        max_length=255,
        read_only=True
    )
    password: serializers.CharField = serializers.CharField(
        max_length=128,
        write_only=True
    )
    token: serializers.CharField = serializers.CharField(
        max_length=255,
        read_only=True
    )

    def validate(self, data: Dict) -> Dict:
        email: serializers.CharField = data.get('email', None)
        password: serializers.CharField = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in'
            )

        user: User = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated'
            )

        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }
