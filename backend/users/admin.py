from django.contrib import admin
from django.contrib.admin import display
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from users.models import Profile, User
from realties.models import Ad, Category, City, Comment, Photo, Realty

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('title', 'timezone',)
    search_fields = ('title',)


@admin.register(Realty)
class RealtyAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'city', 'address', 'category', 'image_preview',
    )
    list_filter = ('city', 'category',)
    search_fields = ('title', 'city', 'address')

    @mark_safe
    @display(description='Фото')
    def image_preview(self, realty):
        return (
            f'<img src="{realty.img.url}" style="max-height: 70px;">'
        )


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'realty', 'address', 'is_published',
        'added_in_favorites'
    )

    @display(description='В избранных')
    def added_in_favorites(self, ad):
        return ad.favorite_users.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'text', 'date_create', 'is_validate',)
    list_filter = ('is_validate',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'date', 'is_validate', 'image_preview',)
    list_filter = ('is_validate',)

    @mark_safe
    @display(description='Фото')
    def image_preview(self, photo):
        return (
            f'<img src="{photo.img.url}" style="max-height: 70px;">'
        )
