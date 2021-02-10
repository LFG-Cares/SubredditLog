from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, Layout, Row, Submit
from django import forms
from django.core.exceptions import ValidationError

from entries.models import Entry


class EntryForm(forms.ModelForm):
    ban_length = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'user',
            'rule',
            Row(
                Column('action', css_class='form-group col-md-8, mb-0'),
                Column('ban_length', css_class='form-group col-md-4 mb-0'),
                css_class='form-row',
            ),
            'notes',
            Submit('submit', 'Save Entry', css_class='btn btn-success'),
        )

    def clean(self):
        cleaned_data = super().clean()
        ban_length = cleaned_data.get('ban_length')
        action = cleaned_data.get('action')

        if action == Entry.ACTION_TEMP_BAN and not ban_length:
            raise ValidationError('Ban Length is required for temporary bans.')

    class Meta:
        model = Entry
        fields = [
            'user',
            'rule',
            'action',
            'ban_length',
            'notes',
        ]
