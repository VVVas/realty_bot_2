from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Profile, User


admin.site.empty_value_display = '_пусто_'
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id', 'username', 'email', 'first_name', 'last_name', 'is_active',
        'is_staff'
    )
    list_display_links = ['username']
    list_filter = ()
    list_editable = ('is_active', 'is_staff')
    search_fields = ('email', 'username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'external_id', 'username', 'first_name', 'last_name',
        'favorite_count', 'comments_count', 'status',
    )
    list_display_links = ['username']
    # readonly_fields = ('external_id',)
    list_per_page = 10

    @display(description='Избранное')
    def favorite_count(self, user):
        return user.favorite_ad.filter(user=user).count()

    @display(description='Комментарии')
    def comments_count(self, user):
        return user.comment.filter(user=user).count()
