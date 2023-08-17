from django.contrib import admin
from django.contrib.auth import get_user_model
from .model.profile import Profile
from .model.adress import Adress

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminChangeForm, UserAdminCreationForm

from import_export.admin import ImportExportModelAdmin
from .resources import AdressResource


User = get_user_model()

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'get_user_email')
    search_fields = ['firstname', 'lastname', 'user__email'] 
    def get_user_email(self, obj):
        return obj.user.email if obj.user else None
    get_user_email.short_description = 'User Email'

admin.site.register(Profile, ProfileAdmin)

class AdressAdmin(ImportExportModelAdmin):
    resource_classes = [AdressResource]
    list_display = ('get_street', 'get_zip', 'place')
    list_display_links = ('get_street', 'get_zip', 'place')
    list_filter = ('place',)
    search_fields = ('street', 'zipcode', 'place',)
    list_per_page = 25



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = True
    verbose_name_plural = 'Profile'
    fk_name = 'user'

    fieldsets = (
        ('Gebruikers info', {'fields': ('firstname', 'lastname', 'gender', 'phone', 'date_of_birth', 'adress', 'profiel', 'avatar', 'bio', 'hobby',)}),
        
    )


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    inlines = (ProfileInline,)
    list_display = ['email', 'formated_date_joined', 'formated_last_login', 'active']
    list_filter = ['active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('admin', 'staff', 'active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'password_2')}
        ),
    )
    search_fields = ['email']
    ordering = ['email']
    filter_horizontal = ()



admin.site.register(Adress, AdressAdmin)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)




admin.site.site_header = "Bredius Rollers Admin"
admin.site.site_title = "Admin"
admin.site.index_title = "Bredius Rollers"