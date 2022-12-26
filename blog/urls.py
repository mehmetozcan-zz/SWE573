from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    generate_preview,
    posts_of_following_profiles
)
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    ##path('profiles/', include("users.urls")),
    path('myspace', posts_of_following_profiles, name='following-posts'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/preview', generate_preview, name='post-preview'),
    path('about/', views.about, name='blog-about'),
]
