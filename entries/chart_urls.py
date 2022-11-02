from django.urls import path

from entries.views import get_mod_actions_chart, get_rules_chart

urlpatterns = [
    path('mod_actions', get_mod_actions_chart, name='chart-mod-actions'),
    path('rules', get_rules_chart, name='chart-rules'),
]
