from django.contrib import admin
from django.urls import include, path

from entries.views import (AddEntryView, EditEntryView, ImportEntriesView, LogView, RulesView, Search, StatsView,
                           UserView, ban_check, health_check)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LogView.as_view(), name='log-view'),
    path('add_entry', AddEntryView.as_view(), name='entry-create'),
    path('edit_entry/<int:pk>', EditEntryView.as_view(), name='entry-edit'),
    path('import', ImportEntriesView.as_view(), name='import-entries'),
    path('ban_check', ban_check, name='ban-check'),
    path('search', Search.as_view(), name='search'),
    path('user/<str:username>', UserView.as_view(), name='user'),
    path('rules', RulesView.as_view(), name='rules-list'),
    path('stats', StatsView.as_view(), name='stats'),
    path('charts/', include('entries.chart_urls')),
    path('health', health_check, name='health-check'),
    path('accounts/', include('allauth.urls')),
]
