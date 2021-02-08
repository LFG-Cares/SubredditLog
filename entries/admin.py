from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from entries.models import Entry, Rule


@admin.register(Rule)
class RuleAdmin(OrderedModelAdmin):
    list_display = (
        'order',
        'name',
        'move_up_down_links'
    )


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'moderator',
        'user',
        'rule',
        'action_string'
    )
