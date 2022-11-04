from django.urls import path
from . import views

app_name='Trainings'

urlpatterns = [
    path('', views.trainings, name='trainings'),
    path('<int:training_id>', views.training, name='training'),

]