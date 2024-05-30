from import_export import resources
from .models import Category, City, Realty


class RealtyResource(resources.ModelResource):
    class Meta:
        model = Realty
        exclude = ['img', 'category', 'city']


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category
        exclude = ['id']


class CityResource(resources.ModelResource):
    class Meta:
        model = City
        exclude = ['id']
