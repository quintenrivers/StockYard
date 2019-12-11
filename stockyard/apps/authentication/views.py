import rest_framework.serializers
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from typing import Tuple

from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
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
