from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Post


class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


def index(request):
    return render(request, 'index.html')
