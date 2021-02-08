from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    @property
    def link(self):
        return f'https://www.reddit.com/u/{self.username}'

    def __str__(self):
        return self.username
