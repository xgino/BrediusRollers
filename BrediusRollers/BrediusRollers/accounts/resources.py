
from import_export import resources

from .model.adress import Adress

class AdressResource(resources.ModelResource):
    class Meta:
        model = Adress
        fields = ('id', 'street', 'house_number', 'zipcode', 'zipcode_number', 'place',)

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        

