from ninja import NinjaAPI
from ninja.security import HttpBearer

from accounts.models import authenticate_token


class TokenAuth(HttpBearer):

    def authenticate(self, request, token):
        return authenticate_token(token)


api = NinjaAPI(
    auth=TokenAuth(),
    docs_url=None,
)
