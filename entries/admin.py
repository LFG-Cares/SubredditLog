from constance import config
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from ordered_model.admin import OrderedModelAdmin
from requests import get

from entries.models import Entry, Rule


@admin.register(Rule)
class RuleAdmin(OrderedModelAdmin):
    change_list_template = 'admin/rules_change_list.html'
    list_display = (
        'order',
        'name',
        'move_up_down_links'
    )

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-rules/', self.import_rules),
        ]
        return my_urls + urls

    def import_rules(self, request):
        if request.method == 'POST':
            if not config.SUBREDDIT:
                return render(request, 'admin/import_rules.html', context={'error': 'subreddit not set'})

            response = get(
                f'https://www.reddit.com/r/{config.SUBREDDIT}/about/rules.json',
                headers={'User-Agent': 'SubredditLog 1.0'}
            )
            if response.status_code != 200:
                return render(request, 'admin/import_rules.html', context={'error': 'error getting rules'})

            try:
                rules = response.json()['rules']
            except KeyError:
                return render(request, 'admin/import_rules.html', context={'error': 'error getting rules'})

            status = []

            for rule in rules:
                try:
                    Rule.objects.create(
                        name=rule['short_name'],
                        description=rule['description'],
                    )
                    status.append(f'Loaded {rule["short_name"]}.')
                except KeyError as ex:
                    status.append(f'Unable to load rule {rules.index(rule) + 1}: {ex}')
                    continue

            return render(request, 'admin/import_rules.html', context={'status': status})
        else:
            return render(request, 'admin/import_rules.html')


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'date',
        'moderator',
        'rule',
        'action_string'
    )

    fields = (
        'user',
        'date',
        'rule',
        'action',
        'ban_length',
        'notes',
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.moderator = request.user
        obj.save()
