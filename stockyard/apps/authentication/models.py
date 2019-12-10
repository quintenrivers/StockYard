import django.db.models
import jwt
from django.db import models
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from typing import List


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: str) -> models:
        if None in (username, email, password):
            raise TypeError('Users must have a username, email address, and password')

        user: models = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username: str, email: str, password: str) -> models:
        user: models = self.create_user(
            username,
            email,
            password
        )

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username: models.CharField = models.CharField(
        db_index=True,
        max_length=255,
        unique=True
    )

    email: models.EmailField = models.EmailField(
        db_index=True,
        unique=True
    )

    # Allows us to deactivate users without completely deleting them
    is_active: models.BooleanField = models.BooleanField(default=True)

    # Allows access to admin site
    is_staff: models.BooleanField = models.BooleanField(default=False)

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    # Fields required by `Django` for custom user model
    # `USERNAME_FIELD` tells us to use which field is used to login
    USERNAME_FIELD: str = 'email'
    REQUIRED_FIELDS: List[str] = ['username']

    objects: UserManager = UserManager()

    def __str__(self) -> django.db.models.EmailField:
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console
        """
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user token by calling `user.token`
        """
        return self._generate_jwt_token()

    def get_full_name(self) -> str:
        """
        Required by Django
        Returns `username`
        """
        return f"{self.username}"

    def get_short_name(self) -> str:
        """
        Required by Django
        Returns `username`
        """
        return f"{self.username}"

    def _generate_jwt_token(self) -> token:
        """
        Generates a JSON Web Token that stores user's ID and has an expiry date
        set to 60 days into the future
        """
        dt: datetime = datetime.now() + timedelta(days=60)
        token = jwt.encode({
                'id': self.pk,
                'exp': int(dt.strftime('%s')),
            },
            settings.SECRET_KEY,
            algorithm='HS256'
        )

        return token.decode('utf-8')
