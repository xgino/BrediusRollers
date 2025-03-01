from django.contrib import admin
from django.contrib.auth.models import Group
from club_management.models import Address, Profile, Club, Coach, Role, Sponsor, TrainingTime, TrainingLocation

# Unregister Groups
admin.site.unregister(Group)

# Rename Admin Panel
admin.site.site_header = "Bredius Rollers Admin"
admin.site.site_title = "Bredius Rollers"
admin.site.index_title = "Management Panel"

# Compact Admin Registration
models = [Address, Profile, Club, Coach, Role, Sponsor, TrainingTime, TrainingLocation]

for model in models:
    admin.site.register(model)
