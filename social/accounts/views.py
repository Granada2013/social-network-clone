from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserSignUpForm, UserProfileForm


def signup(request):
    if request.method == 'POST':
        auth_form = UserSignUpForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if auth_form.is_valid() and profile_form.is_valid():
            user = auth_form.save()
            user.set_password(request.POST['password1'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            return redirect(reverse('login'))
    else:
        auth_form = UserSignUpForm()
        profile_form = UserProfileForm()
    return render(request, template_name='accounts/signup.html', context={'auth_form': auth_form,
                                                                          'profile_form': profile_form})
