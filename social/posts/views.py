from django.contrib import messages
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from .models import Post
from groups.models import Group
from accounts.models import User

from accounts.forms import UserProfileForm
from accounts.models import UserProfile


class UserProfileView(generic.ListView):
    """
    Renders a list of posts written by currently loggined-in user
    """
    model = Post
    template_name = 'posts/user_profile.html'

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class EditProfileView(LoginRequiredMixin, UpdateView):
    """
    Renders a form to edit user's profile
    """
    form_class = UserProfileForm
    template_name = 'posts/edit_profile.html'

    def get_object(self, queryset=None):
        object = get_object_or_404(UserProfile, user__username=self.kwargs.get('username'))
        return object

    def get_success_url(self):
        username = self.kwargs.get('username')
        return reverse('posts:user_profile', kwargs={'username': username})


class PostDetailView(generic.DetailView):
    model = Post
    select_related = ('user', 'group')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))


class CreatePostView(LoginRequiredMixin, generic.CreateView):
    """
    Renders a form to create new post
    """
    fields = ('group', 'message')
    model = Post

    def get_success_url(self):
        group_id = self.request.POST['group']
        return reverse_lazy('groups:single', kwargs={'slug': Group.objects.get(id=group_id).slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    select_related = ('user', 'group')

    def get_success_url(self):
        username = self.kwargs.get('username')
        return reverse_lazy('posts:user_profile', kwargs={'username': username})

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
