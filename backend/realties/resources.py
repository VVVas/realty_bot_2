from import_export import resources
from .models import Category, City, Realty


class RealtyResource(resources.ModelResource):
    class Meta:
        model = Realty


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class CityResource(resources.ModelResource):
    class Meta:
        model = City
