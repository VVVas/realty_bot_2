from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget

from .models import Category, City, Realty


class RealtyResource(resources.ModelResource):
    city = Field(
        column_name='city',
        attribute='city',
        widget=ForeignKeyWidget(model=City, field='title'))

    category = Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(model=Category, field='title'))

    def before_import_row(self, row, **kwargs):
        city = row["city"]
        category = row["category"]
        City.objects.get_or_create(title=city, defaults={"title": city})
        Category.objects.get_or_create(
            title=category, defaults={"title": category}
        )

    class Meta:
        model = Realty


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CityResource(resources.ModelResource):
    class Meta:
        model = City
