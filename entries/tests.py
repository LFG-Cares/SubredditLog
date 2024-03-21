from constance.test import override_config
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from entries.forms import EntryForm
from entries.models import Entry, Rule


class EntryFormTest(TestCase):

    def setUp(self) -> None:
        self.rule1 = Rule.objects.create(name='Be civil')

    def test_cannot_submit_temp_ban_without_length(self):
        form = EntryForm(data={
            'user': 'thecal714',
            'rule': self.rule1,
            'action': Entry.ACTION_TEMP_BAN,
        })

        self.assertIn(
            'Ban Length is required for temporary bans.',
            form.errors['__all__']
        )

    def test_can_submit_user_in_u_slash_format(self):
        form = EntryForm(data={
            'user': 'u/thecal714',
            'rule': self.rule1,
            'action': Entry.ACTION_WARN,
        })

        self.assertTrue(form.is_valid())
        entry = form.save()
        self.assertEqual(entry.user, 'thecal714')

    def test_can_submit_user_in_slash_u_slash_format(self):
        form = EntryForm(data={
            'user': '/u/thecal714',
            'rule': self.rule1,
            'action': Entry.ACTION_WARN,
        })

        self.assertTrue(form.is_valid())
        entry = form.save()
        self.assertEqual(entry.user, 'thecal714')


class ProtectedViewsTest(TestCase):

    def setUp(self) -> None:
        self.note = 'This guy stinks on ice.'
        self.mod1 = get_user_model().objects.create_user(username='mod1', password='testing321')
        self.mod2 = get_user_model().objects.create_user(username='mod2', password='testing123')
        self.su = get_user_model().objects.create_superuser(username='su', password='super123')
        rule1 = Rule.objects.create(name='Be civil')
        self.entry = Entry.objects.create(
            moderator=self.mod1,
            user='thecal714',
            rule=rule1,
            action=Entry.ACTION_PERM_BAN,
            notes=self.note,
        )
        self.button_code = f'<a class="btn btn-outline-warning" ' \
                           f'href="{reverse("entry-edit", kwargs={"pk": self.entry.pk})}">Edit</a>'

    def test_cannot_see_notes_as_anonymous(self):
        response = self.client.get(reverse('log-view'))
        self.assertNotContains(response, self.note)

    def test_cannot_access_add_entry_view_as_anonymous(self):
        response = self.client.get(reverse('entry-create'), follow=True)
        self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('entry-create')}")

    def test_cannot_access_search_as_anonymous_when_private(self):
        with override_config(PUBLIC_MODLOG=False):
            response = self.client.get(reverse('search'))
            self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('search')}")

    def test_cannot_access_edit_as_anonymous(self):
        response = self.client.get(reverse('entry-edit', kwargs={'pk': self.entry.pk}), follow=True)
        self.assertRedirects(response,
                             f"{reverse('account_login')}?next={reverse('entry-edit', kwargs={'pk': self.entry.pk})}")

    def test_cannot_see_edit_button_as_different_nonsuperuser(self):
        self.client.login(username='mod2', password='testing123')
        response = self.client.get(reverse('log-view'))

        self.assertNotContains(response, self.button_code)

    def test_can_access_edit_as_mod(self):
        self.client.login(username='mod1', password='testing321')
        response = self.client.get(reverse('entry-edit', kwargs={'pk': self.entry.pk}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_can_see_edit_button_as_mod(self):
        self.client.login(username='mod1', password='testing321')
        response = self.client.get(reverse('log-view'))
        self.assertContains(response, self.button_code)

    def test_can_access_edit_as_superuser(self):
        self.client.login(username='su', password='super123')
        response = self.client.get(reverse('entry-edit', kwargs={'pk': self.entry.pk}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_can_see_edit_as_superuser(self):
        self.client.login(username='su', password='super123')
        response = self.client.get(reverse('log-view'))
        self.assertContains(response, self.button_code)


class PageTests(TestCase):

    def setUp(self) -> None:
        self.note = 'This guy stinks on ice.'
        self.mod1 = get_user_model().objects.create_user(username='mod1', password='testing321')
        self.mod2 = get_user_model().objects.create_user(username='mod2', password='testing123')
        self.rule1 = Rule.objects.create(name='Be civil')
        self.entry = Entry.objects.create(
            moderator=self.mod1,
            user='thecal714',
            rule=self.rule1,
            action=Entry.ACTION_PERM_BAN,
            notes=self.note,
        )

    def test_profile_link_on_user_page(self):
        self.client.login(username='mod2', password='testing123')
        response = self.client.get(reverse('user', kwargs={'username': self.entry.user}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'https://www.reddit.com/u/{self.entry.user}')
