from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core import validators
from django.core.exceptions import ValidationError

from .models import UserProfile, User


class UserSignUpForm(UserCreationForm):
    botcatcher = forms.CharField(widget=forms.HiddenInput, required=False,
                                 validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = User
        fields = ('username', 'email',
                  'password1', 'password2')

        help_texts = {'username': None}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['password1'].help_text = None

    def clean(self):

        username = self.cleaned_data.get('username')
        if len(username) > 10:
            raise ValidationError('Max length is 10')

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return self.cleaned_data
        else:
            raise ValidationError('This username already exists')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_pic', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].label = 'Profile picture'
        self.fields['bio'].label = 'About me'
        self.fields['bio'].widget.attrs.update({'rows': 3})
