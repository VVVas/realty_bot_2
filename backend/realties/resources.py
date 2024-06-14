import random

from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Ad, Category, City, Realty


class RealtyResource(resources.ModelResource):
    city = Field(
        attribute='city',
        widget=ForeignKeyWidget(model=City, field='title'),
    )

    categories = Field(
        attribute='categories',
        widget=ManyToManyWidget(model=Category, field='title', separator='|'),
    )

    def before_import_row(self, row, **kwargs):
        city = row["city"]
        City.objects.get_or_create(title=city, defaults={"title": city})
        for category in row["categories"].split('|'):
            Category.objects.get_or_create(
                title=category, defaults={"title": category}
            )

    class Meta:
        model = Realty
        exclude = ('img')
        import_id_fields = ('id',)


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CityResource(resources.ModelResource):
    class Meta:
        model = City


class AdResource(resources.ModelResource):
    realty = Field(
        attribute='realty',
        widget=ForeignKeyWidget(model=Realty, field='id'),
    )

    def before_import_row(self, row, **kwargs):
        row['realty'] = random.choice(
            Realty.objects.values_list('id', flat=True)
        )
        row['address'] = Realty.objects.filter(
            id=row['realty']
        ).values_list('address', flat=True)[0]

    class Meta:
        model = Ad
        exclude = ('is_published')
        import_id_fields = ('id',)
