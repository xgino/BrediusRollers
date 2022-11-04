from django.urls import path
from . import views
from accounts.views import LoginView, RegisterView
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

app_name='Accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('team/', views.team, name='team'),
    path('account_games/', views.account_games, name='account_games'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', views.ChangePasswordView.as_view(), name='password_change'),
]