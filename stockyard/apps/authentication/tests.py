import json
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User
from .serializers import RegistrationSerializer


class UserTestCase(APITestCase):
    username: str = "testcase"
    email: str = "testcase@localhost.app"
    password: str = "strong_password_1"
    wrong_password: str = "wrong_password_1"

    def __register_user__(self) -> dict:
        data: dict = {
            "user": {
                "username": self.username,
                "email": self.email,
                "password": self.password,
            }
        }

        return self.client.post(
            "/api/users/",
            data,
            format="json"
        )

    def __register_token_auth__(self) -> str:
        resp: dict = json.loads(self.__register_user__().content)
        token: str = resp["user"]["token"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {token}"
        )

    def test_registration(self) -> None:
        response: dict = self.__register_user__()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self) -> None:
        self.__register_user__()

        data: dict = {
            "user": {
                "email": self.email,
                "password": self.password,
            }
        }

        response: dict = self.client.post(
            "/api/users/login/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self) -> None:
        self.__register_user__()

        data: dict = {
            "user": {
                "email": self.email,
                "password": self.wrong_password,
            }
        }

        response: dict = self.client.post(
            "/api/users/login/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self) -> None:
        self.__register_token_auth__()

        data: dict = {
            "user": {
                "email": "newemail@localhost.app",
            }
        }

        response: dict = self.client.put(
            "/api/user/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_fail(self) -> None:
        self.__register_user__()

        data: dict = {
            "user": {
                "email": "newemail@localhost.app",
            }
        }

        response: dict = self.client.put(
            "/api/user/",
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_current_user(self) -> None:
        self.__register_token_auth__()

        response: dict = self.client.get("/api/user/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user_fail(self) -> None:
        self.__register_user__()

        response: dict = self.client.get("/api/user/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)