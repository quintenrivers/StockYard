import rest_framework.serializers
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Tuple, Dict

from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
    UserSerializer,
)
from .renderers import UserJSONRenderer


class RegistrationAPIView(APIView):
    permission_classes: Tuple = (AllowAny,)
    renderer_classes: Tuple = (UserJSONRenderer,)
    serializer_class: rest_framework.serializers = RegistrationSerializer

    def post(self, request) -> Response:
        user = request.data.get('user', {})

        serializer: RegistrationSerializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes: Tuple = (AllowAny,)
    renderer_classes: Tuple = (UserJSONRenderer,)
    serializer_class: rest_framework.serializers = LoginSerializer

    def post(self, request) -> Response:
        user = request.data.get('user', {})

        serializer: rest_framework.serializers = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes: Tuple = (IsAuthenticated,)
    renderer_classes: Tuple = (UserJSONRenderer,)
    serializer_class: rest_framework.serializers = UserSerializer

    def retrieve(self, request, *args, **kwargs) -> Response:
        serializer: rest_framework.serializers = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs) -> Response:
        serializer_data = request.data.get('user', {})

        serializer: rest_framework.serializers = self.serializer_class(
            request.user,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid()
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
