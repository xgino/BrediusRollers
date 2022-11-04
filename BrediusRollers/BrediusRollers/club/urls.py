from django.urls import path
from . import views
from accounts.views import LoginView, RegisterView
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

app_name='Clubs'

urlpatterns = [
    path('', views.clubs, name='clubs'),
    path('<int:club_id>', views.club, name='club'),

]