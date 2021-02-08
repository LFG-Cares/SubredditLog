from django.contrib.auth import get_user_model
from django.test import TestCase

PASSWORD = 'p@ssw0rd123'


def create_user(username='test_user', password=PASSWORD):
    return get_user_model().objects.create_user(
        username=username,
        first_name='Test',
        last_name='User',
        password=password
    )


class TestUserModel(TestCase):

    def test_url_link(self):
        user = create_user()

        self.assertIn(f'/u/{user.username}', user.link)
