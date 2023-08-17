from django.contrib import admin
from .models import Club, Season, Subscription, Coach, Role, Sponsors, Photo

from import_export.admin import ImportExportModelAdmin
from .resources import CoachResource, RoleResource, SeasonResource, ClubResource, SubscriptionResource

class CoachAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'season')
    list_display_links = ('profile',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
        ('profile__firstname'),
    ]
    list_per_page = 25

class CoachInline(admin.TabularInline):
    model = Coach
    verbose_name_plural = 'Coaches'
    fields = ('profile',)  # Add other fields as needed
    autocomplete_fields = ('profile',)  # Add autocomplete for profile selection
    extra = 0  # Set the number of empty forms to 0

    def profile_name(self, obj):
        return f"{obj.profile.firstname} {obj.profile.lastname}"  # Display first name and last name
    profile_name.short_description = 'Profile Name'
    
    def profile_email(self, obj):
        return obj.profile.user.email  # Display email
    profile_email.short_description = 'Profile Email'
    profile_email.admin_order_field = 'profile__user__email'  # Enable sorting by email

class RoleInline(admin.TabularInline):
    model = Role
    verbose_name_plural = 'Role'
    fields = ('profile', 'title', 'short_description', 'description')  # Add other fields as needed
    autocomplete_fields = ('profile',)  # Add autocomplete for profile selection
    extra = 0  # Set the number of empty forms to 0

class SeasonAdmin(admin.ModelAdmin):
    inlines = [CoachInline, RoleInline]
    list_display = ('id', 'start_date', 'end_date',)
    list_display_links = ('start_date', 'end_date')
    list_per_page = 25

class SponsorsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_description')
    list_display_links = ('title',)
    list_per_page = 25

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_num', 'season')
    list_display_links = ('sub_num',)
    search_fields = ('sub_num',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
    ]
    list_per_page = 25

class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'season', 'members', 'city']
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
        ('name'),
    ]
    search_fields = ['name']
    list_per_page = 25

class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'title')
    list_display_links = ('profile',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
        ('title'),
    ]
    list_per_page = 25

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'photo')
    list_display_links = ('title',)
    list_filter = ('season',)
    list_filter = [
        ('season', admin.RelatedFieldListFilter),
    ]
    list_per_page = 25

# Register the admin classes
admin.site.register(Season, SeasonAdmin)
admin.site.register(Club, ClubAdmin)
admin.site.register(Sponsors, SponsorsAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
# admin.site.register(Coach, CoachAdmin)
# admin.site.register(Role, RoleAdmin)
admin.site.register(Photo, PhotoAdmin)