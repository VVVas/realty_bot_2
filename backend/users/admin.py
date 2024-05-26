from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import Profile, User

admin.site.empty_value_display = '_пусто_'


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
        'is_staff'
    )
    list_filter = ('username', 'email')
    list_editable = ('is_active', 'is_staff')
    search_fields = ('email', 'username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'external_id', 'username', 'first_name', 'last_name', 'is_active'
    )


admin.site.unregister(Group)
