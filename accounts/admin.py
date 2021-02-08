from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from accounts.models import User


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass
