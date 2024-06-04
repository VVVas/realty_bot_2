from django.contrib import admin
from django.db import models
from django.apps import apps
from django.forms import TextInput, Textarea
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import display
from django.utils.safestring import mark_safe
from rangefilter.filters import DateRangeFilterBuilder

from .models import (
    Ad, Category, City, Comment, Photo, Realty
)
from .resources import CategoryResource, CityResource, RealtyResource


@admin.action(description="Опубликовать выбранные")
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)


@admin.action(description="Снять выбранные с публикации")
def make_not_published(modeladmin, request, queryset):
    queryset.update(is_published=False)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'realty_count')
    search_fields = ('title',)
    resource_class = CategoryResource

    @display(description='Используется')
    def realty_count(self, category):
        return Realty.objects.filter(categories=category).count()


@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    list_display = ('id', 'title', 'timezone', 'realty_count',)
    search_fields = ('title',)
    resource_class = CityResource

    @display(description='Используется')
    def realty_count(self, city):
        return Realty.objects.filter(city=city).count()


class AdInline(admin.TabularInline):
    model = Ad
    extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }


@admin.register(Realty)
class RealtyAdmin(ImportExportModelAdmin):
    list_display = (
        'title', 'city', 'address', 'get_categories', 'image_preview',
    )
    search_fields = ('title', 'city__title', 'address')
    list_filter = ()
    filter_horizontal = ('categories',)
    resource_class = RealtyResource
    autocomplete_fields = ['city']
    inlines = (AdInline,)

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '40'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
    }

    @mark_safe
    @display(description='Категории')
    def get_categories(self, realty):
        return ('<br />'.join(
            item.title for item in realty.categories.all())
        )

    @mark_safe
    @display(description='Фото')
    def image_preview(self, realty):
        if realty.img:
            return (
                f'<img src="{realty.img.url}" style="max-height: 70px;">'
            )
        return 'Фото отсутствует'


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'realty', 'address', 'date', 'is_published',
        'added_in_favorites'
    )
    list_filter = (
        ("date", DateRangeFilterBuilder(title="Дата добавления",)),
    )
    list_editable = ('is_published',)
    autocomplete_fields = ['realty']
    actions = [make_published, make_not_published]

    @display(description='В избранных')
    def added_in_favorites(self, ad):
        return ad.favorite_users.count()


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'text', 'date_create', 'is_published',)
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    ordering = ('is_published', 'date_create')
    actions = [make_published, make_not_published]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'ad', 'date', 'is_published', 'image_preview',)
    list_filter = ('is_published',)
    list_editable = ('is_published',)
    actions = [make_published, make_not_published]

    @mark_safe
    @display(description='Фото')
    def image_preview(self, photo):
        return (
            f'<img src="{photo.img.url}" style="max-height: 70px;">'
        )
