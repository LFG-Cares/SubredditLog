from django.contrib.auth import get_user_model
from django.db import models
from ordered_model.models import OrderedModel


class Rule(OrderedModel):
    """Represents a subreddit rule to which a moderator action may be link."""
    name = models.CharField(max_length=255, help_text='The name of the rule')
    description = models.TextField(blank=True, default='', help_text='Text to further explain or define the rule')

    def __str__(self):
        return self.name


class Entry(models.Model):
    ACTION_WARN = 1
    ACTION_TEMP_BAN = 2
    ACTION_PERM_BAN = 3
    ACTION_CHOICES = (
        (ACTION_WARN, 'Warn'),
        (ACTION_TEMP_BAN, 'Temporary Ban'),
        (ACTION_PERM_BAN, 'Permanent Ban'),
    )

    moderator = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, editable=False,
                                  related_name='entries')
    date = models.DateField(auto_now_add=True)
    user = models.CharField(max_length=20, blank=False, db_index=True)
    rule = models.ForeignKey(Rule, on_delete=models.SET_NULL, null=True, related_name='+')
    action = models.PositiveSmallIntegerField(choices=ACTION_CHOICES, default=ACTION_WARN)
    ban_length = models.PositiveSmallIntegerField(null=True, default=None, help_text='The length of a temporary ban')
    notes = models.TextField(blank=True, default='', help_text='A private note to attach to this entry.')

    @property
    def action_string(self):
        if self.action == Entry.ACTION_TEMP_BAN:
            return f'{self.ban_length}-day Ban'
        elif self.action == Entry.ACTION_PERM_BAN:
            return 'Permanent Ban'
        else:
            return 'Warning Issued'

    class Meta:
        ordering = ['-date', '-id']
        verbose_name_plural = 'entries'

    def __str__(self):
        return f'Action for /u/{self.user} on {self.date}'
