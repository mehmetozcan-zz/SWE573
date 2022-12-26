from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from users.models import Profile
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse
from itertools import chain
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def get_title(html):
    """Scrape page title."""
    title = None
    if html.title.string:
        title = html.title.string
    elif html.find("meta", property="og:title"):
        title = html.find("meta", property="og:title").get('content')
    elif html.find("meta", property="twitter:title"):
        title = html.find("meta", property="twitter:title").get('content')
    elif html.find("h1"):
        title = html.find("h1").string
    return title

def get_description(html):
    """Scrape page description."""
    description = None
    if html.find("meta", property="description"):
        description = html.find("meta", property="description").get('content')
    elif html.find("meta", property="og:description"):
        description = html.find("meta", property="og:description").get('content')
    elif html.find("meta", property="twitter:description"):
        description = html.find("meta", property="twitter:description").get('content')
    elif html.find("p"):
        description = html.find("p").contents
    return description

def get_image(html):
    """Scrape share image."""
    image = None
    if html.find("meta", property="image"):
        image = html.find("meta", property="image").get('content')
    elif html.find("meta", property="og:image"):
        image = html.find("meta", property="og:image").get('content')
    elif html.find("meta", property="twitter:image"):
        image = html.find("meta", property="twitter:image").get('content')
    elif html.find("img", src=True):
        image = html.find_all("img").get('src')
    return image

def generate_preview(request):
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }

    url = request.GET.get('link')
    print(url)
    req = requests.get(url, headers)
    html = BeautifulSoup(req.content, 'html.parser')
    meta_data = {
        'title': get_title(html),
        'description': get_description(html),
        'image': get_image(html),
    }

    print(meta_data)

    return JsonResponse(meta_data)

def posts_of_following_profiles(request):
    profile = Profile.objects.get(user=request.user)
    users = [user for user in profile.following.all()]
    posts = []
    paginate_by = 5
    qs = None
    for u in users:
        p = Post.objects.filter(author=u)
        posts.append(p)
    my_posts = Post.objects.filter(author=request.user)
    posts.append(my_posts)
    if len(posts) > 0:
        qs = sorted(chain(*posts), reverse=True, key=lambda obj: obj.date_posted)
    return render(request, 'blog/myspace.html', {'posts':qs})
