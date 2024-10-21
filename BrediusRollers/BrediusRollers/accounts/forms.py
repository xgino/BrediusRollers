from inspect import Attribute
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model
from .model.profile import Profile
from .model.adress import Adress

User = get_user_model()

class LoginForm(forms.Form):
    email    = forms.EmailField(widget=forms.TextInput(attrs={'name': 'loginUsername', 'class': 'input-material', 'id': 'login-username', 'data-msg': 'E-mailadres is verplicht.'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'loginPassword', 'class': 'input-material', 'id': 'login-password', 'data-msg': 'Wachtwoord is verplicht.'}))

class RegisterForm(forms.ModelForm):
    """
    The default 

    """
    email    = forms.EmailField(widget=forms.TextInput(attrs={'name': 'registerEmail', 'class': 'input-material', 'id': 'register-email', 'data-msg': 'E-mailadres is verplicht.'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'registerPassword', 'class': 'input-material', 'id': 'register-password', 'data-msg': 'Wachtwoord is verplicht.'}))
    password_2 = forms.CharField(widget=forms.PasswordInput(attrs={'name': 'registerPassword', 'class': 'input-material', 'id': 'register-password', 'data-msg': 'Wachtwoord is verplicht.'}))
 
    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user



class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']


class UpdateProfileForm(forms.ModelForm):
    firstname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    lastname = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    gender    = forms.ChoiceField(choices=Profile.GENDER_CHOICES, label='Gender', required=True, widget=forms.Select(attrs={'class':'form-control mb-3 mb-3'}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}), required=False)

    class Meta:
        model = Profile
        fields = ['firstname', 'lastname', 'gender', 'avatar']



class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'active', 'admin']

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]