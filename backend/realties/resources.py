from import_export import resources
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget

from .models import Category, City, Realty


class RealtyResource(resources.ModelResource):
    city = Field(
        column_name='city',
        attribute='city',
        widget=ForeignKeyWidget(model=City, field='title')
    )

    categories = Field(
        column_name='categories',
        attribute='categories',
        widget=ManyToManyWidget(Category, field='title', separator='|')
    )

    # def before_import_row(self, row, **kwargs):
    #     city = row["city"]
    #     City.objects.get_or_create(title=city, defaults={"title": city})
    #     categories = row["categories"].split('|')
    #     for category in categories:
    #         Category.objects.get_or_create(
    #             title=category, defaults={"title": category}
    #         )


    class Meta:
        model = Realty
        # import_id_fields = ('title',)
        # fields = (
        #     'id', 'title', 'phone_number',
        #     'mobile_number', 'number', 'address',
        #     'email', 'site', 'contact_name', 'city',
        #     'categories', 'additional_information'
        # )


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CityResource(resources.ModelResource):
    class Meta:
        model = City
