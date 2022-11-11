from import_export import resources
from .models import Training, Trainings_location, Trainings_time

class TrainingResource(resources.ModelResource):
    class Meta:
        model = Training
        fields = ('id', 'training_time', 'training_location', 'date')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }
        
class TrainingsLocationResource(resources.ModelResource):
    class Meta:
        model = Trainings_location
        fields = ('id', 'adress')
        
        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }


class TrainingsTimeResource(resources.ModelResource):
    class Meta:
        model = Trainings_time
        fields = ('id', 'start_time', 'end_time')

        widgets = {
            'published': {'format': '%d.%m.%Y'},
        }


