from django.contrib import admin
from django.db import models
from django.apps import apps
from django.forms import TextInput, Textarea
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import display
from django.utils.safestring import mark_safe

from .models import (
    Ad, Category, City, Comment, Photo, Realty,
)
from .resources import RealtyResource


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    search_fields = ('title',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('title', 'timezone',)
    search_fields = ('title',)


@admin.register(Realty)
class RealtyAdmin(ImportExportModelAdmin):
    list_display = (
        'title', 'city', 'address', 'category', 'image_preview',
    )
    search_fields = ('title', 'city', 'address')
    list_filter = ()
    resource_class = RealtyResource

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }

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
    ordering = ('is_validate', 'date_create')


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
