'''
UserForm:
This is a form for the User model. The Meta class inside the UserForm specifies metadata for the form. In this case, it's saying that the form 
is associated with the User model and should include fields for the first_name and last_name.

ProfileForm:
This is a form for the Profile model. Similar to UserForm, the Meta class specifies that the form is associated with the Profile model and should 
include a field for the bio.
'''
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, SavedCoin

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
    
class SavedCoinForm(forms.ModelForm):
    class Meta:
        model = SavedCoin
        fields = ['uuid', 'symbol', 'name']  # Add the rest of the fields
