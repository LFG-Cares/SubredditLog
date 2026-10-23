from hashlib import sha256

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import TOKEN_PREFIX, authenticate_token

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


class TestApiTokenView(TestCase):

    def setUp(self) -> None:
        self.user = create_user()
        self.client.login(username=self.user.username, password=PASSWORD)
        self.url = reverse('api_token')

    def test_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(response, f'{reverse("account_login")}?next={self.url}')

    def test_get_without_token_offers_generate(self):
        self.assertContains(self.client.get(self.url), 'Generate Token')

    def test_get_with_token_offers_regenerate(self):
        self.user.issue_token()
        self.assertContains(self.client.get(self.url), 'Regenerate Token')

    def test_get_does_not_change_token(self):
        self.user.issue_token()
        self.user.refresh_from_db()
        before = self.user.token

        self.client.get(self.url)
        self.user.refresh_from_db()

        self.assertEqual(before, self.user.token)

    def test_post_issues_token_and_shows_it_once(self):
        response = self.client.post(self.url)
        raw = response.context['token']

        self.assertContains(response, raw)
        self.assertEqual(authenticate_token(raw), self.user)
        self.assertNotContains(self.client.get(self.url), raw)

    def test_post_revokes_previous_token(self):
        old = self.user.issue_token()
        self.client.post(self.url)

        self.assertIsNone(authenticate_token(old))

    def test_responses_are_not_cached(self):
        for response in (self.client.get(self.url), self.client.post(self.url)):
            self.assertIn('no-store', response['Cache-Control'])


class TestUserToken(TestCase):

    def setUp(self) -> None:
        self.user = create_user()

    def test_new_user_has_no_token(self):
        self.assertIsNone(self.user.token)
        self.assertIsNone(self.user.token_created_at)

    def test_multiple_users_without_tokens_allowed(self):
        create_user(username='second_user')
        self.assertEqual(get_user_model().objects.filter(token__isnull=True).count(), 2)

    def test_hash_token_is_sha256_hexdigest(self):
        self.assertEqual(
            get_user_model().hash_token('slr_example'),
            sha256(b'slr_example').hexdigest()
        )

    def test_hash_token_is_deterministic(self):
        User = get_user_model()
        self.assertEqual(User.hash_token('slr_example'), User.hash_token('slr_example'))
        self.assertNotEqual(User.hash_token('slr_example'), User.hash_token('slr_example2'))

    def test_issue_token_returns_prefixed_token(self):
        raw = self.user.issue_token()

        self.assertTrue(raw.startswith(TOKEN_PREFIX))
        self.assertGreaterEqual(len(raw), len(TOKEN_PREFIX) + 43)  # 32 bytes urlsafe-encoded

    def test_issue_token_stores_hash_not_raw_token(self):
        raw = self.user.issue_token()
        self.user.refresh_from_db()

        self.assertNotEqual(self.user.token, raw)
        self.assertEqual(self.user.token, get_user_model().hash_token(raw))

    def test_issue_token_sets_created_at(self):
        before = timezone.now()
        self.user.issue_token()
        after = timezone.now()
        self.user.refresh_from_db()

        self.assertIsNotNone(self.user.token_created_at)
        self.assertTrue(before <= self.user.token_created_at <= after)

    def test_issue_token_generates_unique_tokens(self):
        first = self.user.issue_token()
        second = self.user.issue_token()

        self.assertNotEqual(first, second)

    def test_reissuing_token_revokes_previous_token(self):
        old = self.user.issue_token()
        new = self.user.issue_token()
        self.user.refresh_from_db()

        self.assertIsNone(authenticate_token(old))
        self.assertEqual(authenticate_token(new), self.user)

    def test_authenticate_token_accepts_issued_token(self):
        raw = self.user.issue_token()
        self.user.refresh_from_db()

        self.assertEqual(authenticate_token(raw), self.user)

    def test_authenticate_token_rejects_wrong_token(self):
        self.user.issue_token()

        self.assertFalse(authenticate_token(TOKEN_PREFIX + 'not-the-token'))

    def test_authenticate_token_rejects_stored_hash(self):
        self.user.issue_token()
        self.user.refresh_from_db()

        self.assertFalse(authenticate_token(self.user.token))

    def test_authenticate_token_rejects_when_no_token_issued(self):
        self.assertFalse(authenticate_token(''))
        self.assertFalse(authenticate_token(TOKEN_PREFIX + 'anything'))

    def test_authenticate_token_returns_owning_user(self):
        other = create_user(username='other_user')
        raw = self.user.issue_token()
        other_raw = other.issue_token()

        self.assertEqual(authenticate_token(raw), self.user)
        self.assertEqual(authenticate_token(other_raw), other)

    def test_authenticate_token_rejects_inactive_user(self):
        raw = self.user.issue_token()
        self.user.is_active = False
        self.user.save()

        self.assertIsNone(authenticate_token(raw))

    def test_token_hash_must_be_unique(self):
        other = create_user(username='other_user')
        self.user.issue_token()
        other.token = self.user.token

        with self.assertRaises(IntegrityError):
            other.save()
