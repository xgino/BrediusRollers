
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('PAGES.urls')),
    path('wedstrijden/', include('games.urls')),
    path('clubs/', include('club.urls')),
    path('teams/', include('teams.urls')),
    path('players/', include('players.urls')),
    path('trainings/', include('trainings.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns() 
