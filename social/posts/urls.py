from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('new/', views.CreatePostView.as_view(), name='create_post'),
    path('by/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),
    path('by/<str:username>/edit', views.EditProfileView.as_view(), name='edit_profile'),
    path('by/<str:username>/<int:pk>', views.PostDetailView.as_view(), name='single'),
    path('by/<str:username>/<int:pk>/delete', views.DeletePostView.as_view(), name='delete_post'),
]
