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


class ProtectedViewsTest(TestCase):

    def setUp(self) -> None:
        self.note = 'This guy stinks on ice.'
        rule1 = Rule.objects.create(name='Be civil')
        Entry.objects.create(
            user='thecal714',
            rule=rule1,
            action=Entry.ACTION_PERM_BAN,
            notes=self.note,
        )

    def test_cannot_see_notes_as_anonymous(self):
        response = self.client.get(reverse('log-view'))
        self.assertNotContains(response, self.note)

    def test_cannot_access_add_entry_view_as_anonymous(self):
        response = self.client.get(reverse('entry-create'), follow=True)
        self.assertRedirects(response, f"{reverse('account_login')}?next={reverse('entry-create')}")
