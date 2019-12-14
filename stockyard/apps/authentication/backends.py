import jwt
from typing import Optional

from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix: str = 'Token'

    def authenticate(self, request) -> Optional[tuple]:
        """
        Two possible return values:
        1) `None` if we do not wish to authenticate
        2) `(user, token)` if authentication is successful

        If neither case is met, there's an error
        """

        request.user = None

        # `auth_header` is a list with two element:
        # 1) the name of the authentication header
        # 2) the JWT to authenticate against
        auth_header: list = authentication\
            .get_authorization_header(request)\
            .split()
        auth_header_prefix: str = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # No credentials provided
            return None
        elif len(auth_header) > 2:
            return None

        prefix: str = auth_header[0].decode('utf-8')
        token: str = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            # Unexpected auth header prefix
            return None

        return self._authenticate_credentials(request, token)

    @staticmethod
    def _authenticate_credentials(request: object, token: str) -> tuple:
        try:
            payload: dict = jwt.decode(token, settings.SECRET_KEY)
        except exceptions.AuthenticationFailed:
            msg: str = 'Invalid authentication. Could not decode token'
            raise exceptions.AuthenticationFailed(msg)

        try:
            user: User = User.objects.get(pk=payload['id'])
        except exceptions.AuthenticationFailed:
            msg: str = 'No user matching this token was found'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg: str = 'This user has been deactivated'
            raise exceptions.AuthenticationFailed(msg)

        return user, token
