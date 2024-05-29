from import_export import resources
from .models import Realty


class RealtyResource(resources.ModelResource):
    class Meta:
        model = Realty
        exclude = ['img']
