from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, UpdateView)
from django_filters.views import FilterView

from .filters import PostFilterSet
from .forms import PostForm
from .models import Author, Post


class PostList(ListView):
    model = Post
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        post_type = kwargs['post_type']
        self.queryset = Post.objects.filter(post_type=post_type)
        return super(PostList, self).get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post


class PostFilter(FilterView, PostList):
    filterset_class = PostFilterSet


class PostFormView(FormView):
    model = Post
    form_class = PostForm


class PostCreate(CreateView, PostFormView):
    def post(self, request, *args, **kwargs):
        self.post_type = kwargs['post_type']
        return super(PostCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(pk=4)  # Временная заглушка на автора @guest
        post.post_type = self.post_type
        return super().form_valid(form)


class PostUpdate(UpdateView, PostFormView):
    pass


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('home')


def index(request):
    return render(request, 'index.html')
