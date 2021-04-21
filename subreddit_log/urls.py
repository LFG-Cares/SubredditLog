from django.contrib import admin
from django.urls import include, path

from entries.views import AddEntryView, LogView, RulesView, Search, ban_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LogView.as_view(), name='log-view'),
    path('add_entry', AddEntryView.as_view(), name='entry-create'),
    path('ban_check', ban_check, name='ban-check'),
    path('search', Search.as_view(), name='search'),
    path('rules', RulesView.as_view(), name='rules-list'),
    path('accounts/', include('allauth.urls')),
]
