from django.contrib import admin
from django.contrib.admin import display
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from rangefilter.filters import DateRangeFilterBuilder

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
    list_editable = ('status',)
    list_display_links = ['id', 'first_name']
    # readonly_fields = ('external_id',)
    list_per_page = 10
    list_filter = (
        ("date", DateRangeFilterBuilder()),
    )

    change_form_template = "entities/profile_changeform.html"

    @display(description='Избранное')
    def favorite_count(self, user):
        return user.favorite_ad.filter(user=user).count()

    @display(description='Комментарии')
    def comments_count(self, user):
        return user.comment.filter(user=user).count()

    def response_change(self, request, user):
        if "_delete-profile" in request.POST:
            user.delete()
            self.message_user(
                request,
                "Пользователь удалён"
            )
        if "_delete-profile-and-comments" in request.POST:
            Profile.delete_profile_and_comments(user=user)
            self.message_user(
                request,
                "Пользователь и его комментарии удалены"
            )
        return super().response_change(request, user)

    def has_delete_permission(self, request, obj=None):
        return False
