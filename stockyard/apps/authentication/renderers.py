import json

from rest_framework.renderers import JSONRenderer


class UserJSONRenderer(JSONRenderer):
    charset: str = 'utf-8'

    def render(
        self,
        data: dict,
        media_type: str = None,
        renderer_context: str = None
    ) -> str:

        token: bytes = data.get('token', None)
        errors = data.get('errors', None)

        if errors is not None:
            return super(UserJSONRenderer, self).render(data)

        if token is not None and isinstance(token, bytes):
            data['token'] = token.decode(self.charset)

        return json.dumps({
            'user': data
        })
