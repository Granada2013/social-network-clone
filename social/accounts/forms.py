from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators

from .models import UserProfile, User


class UserSignUpForm(UserCreationForm):
    botcatcher = forms.CharField(widget=forms.HiddenInput, required=False,
                                 validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = User
        fields = ('username', 'email',
                  'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Social Space username'
        self.fields['email'].label = 'Email'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].label = 'Profile picture'




