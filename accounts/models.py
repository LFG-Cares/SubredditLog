from hashlib import sha256
from secrets import token_urlsafe

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

TOKEN_PREFIX = 'slr_'


def authenticate_token(raw: str):
    """Used to validate the provided token."""
    return User.objects.filter(token=User.hash_token(raw), is_active=True).first()


class User(AbstractUser):
    token = models.CharField(max_length=64, unique=True, null=True, blank=True)
    token_created_at = models.DateTimeField(null=True, blank=True)

    @property
    def link(self):
        return f'https://www.reddit.com/u/{self.username}'

    def __str__(self):
        return self.username

    @staticmethod
    def hash_token(raw: str) -> str:
        """Returns a hash of the provided token."""
        return sha256(raw.encode()).hexdigest()

    def issue_token(self) -> str:
        """Generates and stores a user's API token.
        Returns the raw token while storing the token's hash.
        """
        raw_token = TOKEN_PREFIX + token_urlsafe(32)
        self.token = self.hash_token(raw_token)
        self.token_created_at = timezone.now()
        self.save(update_fields=['token', 'token_created_at'])

        return raw_token
