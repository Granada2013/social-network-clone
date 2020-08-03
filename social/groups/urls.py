from django.urls import path
from .views import (CreateGroupView, ListGroupsView, SingleGroupView,
                    JoinGroupView, LeaveGroupView, UserGroupsView)


app_name = 'groups'
urlpatterns = [
    path('', ListGroupsView.as_view(), name='all'),
    path('<str:username>', UserGroupsView.as_view(), name='user_groups'),
    path('<slug>/$/', SingleGroupView.as_view(), name='single'),
    path('create/', CreateGroupView.as_view(), name='create_group'),
    path('<slug>/$/join/', JoinGroupView.as_view(), name='join_group'),
    path('<slug>/$/leave/', LeaveGroupView.as_view(), name='leave_group'),
]

