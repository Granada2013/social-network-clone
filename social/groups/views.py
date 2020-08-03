from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Group, GroupMember
from .forms import CreateGroupForm
from accounts.models import User


# Create your views here.

class CreateGroupView(LoginRequiredMixin, generic.CreateView):
    """
    Renders form to create new thread
    """
    login_url = 'home'
    model = Group
    form_class = CreateGroupForm


class SingleGroupView(generic.DetailView):
    """
    Renders thread details
    """
    model = Group


class ListGroupsView(generic.ListView):
    """
    Renders a list of all threads ordered by total num of posts and users in a descending order
    """
    model = Group

    def get_queryset(self):
        queryset = Group.objects.annotate(number_of_posts=Count('posts'),
                                          number_of_members=Count('members'))
        return queryset.order_by('-number_of_posts', '-number_of_members')


class UserGroupsView(generic.ListView):
    """
    Renders a list of groups joined by an owner of a profile page
    """
    model = Group
    template_name = 'groups/user_groups.html'


    def get_context_data(self, **kwargs):
        self.post_user = get_object_or_404(User, username__iexact=self.kwargs.get('username'))
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        context['user_groups'] = Group.objects.filter(members__in=[self.post_user]).order_by('name')
        return context


class JoinGroupView(LoginRequiredMixin, generic.RedirectView):
    """
    A view to join a thread
    """
    login_url = 'home'

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'You are already a member of this group!')
        else:
            messages.success(self.request, 'Congratulations! You joined a group.')
        return super().get(request, *args, **kwargs)


class LeaveGroupView(LoginRequiredMixin, generic.RedirectView):
    """
    A view to leave a thread
    """
    def get_redirect_url(self, *args, **kwargs):
        print(self.kwargs)
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:
            membership = GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get('slug')
            ).get()
            print(f'membership={membership}')  # TO BE DELETED
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'You are not a member of a group')
        else:
            membership.delete()
            messages.success(self.request, 'You left a group.')
        return super().get(request, *args, **kwargs)
