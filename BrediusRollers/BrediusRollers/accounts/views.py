
from urllib import request
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, FormView
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Q


from .forms import LoginForm, RegisterForm
from .forms import UpdateUserForm, UpdateProfileForm

from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from .model.profile import Profile
from .model.adress import Adress
from players.models import Player
from games.models import Goals, Match_team, Game


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('Accounts:dashboard')

    def form_valid(self, form):
        request = self.request
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now login')
            return redirect('Accounts:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('Accounts:login')


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('Accounts:login')


@login_required
def dashboard(request):
    player, created = Profile.objects.get_or_create(user=request.user)  #Create empty profile for new users

    user = request.user
    profile = user.profile
    team = user.profile.player.team
    team_player = Player.objects.all().filter(team=team)
    goals = Goals.objects.all().filter(player=profile.player).aggregate(Sum('goals'))
    match_team = Match_team.objects.all().filter(team=profile.player.team)
    amount_match = Game.objects.all().filter(Q(home_team__in=match_team) | Q(away_team__in=match_team))

    try:
        players = Player.objects.get(user=user.id)
    except:
        players = None

    context = {
        'user': user,
        'profile': profile,
        'team': team,
        'player_count': len(team_player),
        'goals': goals['goals__sum'],
        'points': len(amount_match),
    }

    return render(request, 'dashboard.html', context)


@login_required
def team(request):
    team_player = Player.objects.all().filter(team=request.user.profile.player.team)
    profile = request.user.profile
    context = {'team_player': team_player, 'profile': profile,}
    return render(request, 'team.html', context)


@login_required
def account_games(request):
    profile = request.user.profile
    match_team = Match_team.objects.all().filter(team=profile.player.team)
    games = Game.objects.all().filter(Q(home_team__in=match_team) | Q(away_team__in=match_team)).order_by('gameday__date')       

    context = {'profile': profile, 'games': games}
    return render(request, 'account_games.html', context)



@login_required
def profile(request):
    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)


        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('Accounts:profile')


    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }

    return render(request, 'profile.html', context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('Accounts:dashboard')
