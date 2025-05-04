from ninja.security import HttpBearer
from .models import UserToken


class APIAuthBearer(HttpBearer):
    def authenticate(self, request, token):
        app_user = None
        # token is from the request header
        # Implement your authentication logic here
        # For example, you might want to check if the token is valid
        # and return the corresponding user object.
        user_token = UserToken.objects.filter(token=token).first()
        if user_token:
            app_user = user_token.user
        return app_user
