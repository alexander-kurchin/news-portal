from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from django_filters.views import FilterView

from .filters import PostFilterSet
from .forms import PostForm
from .models import Author, Post, User


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


class PostFormView(PermissionRequiredMixin, FormView):
    model = Post
    form_class = PostForm


class PostCreate(CreateView, PostFormView):
    permission_required = 'news.add_post'

    def post(self, request, *args, **kwargs):
        self.post_type = kwargs['post_type']
        self.user = get_object_or_404(User, username=request.user.username)
        return super(PostCreate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get_or_create(user=self.user)[0]
        post.post_type = self.post_type
        return super().form_valid(form)


class PostUpdate(UpdateView, PostFormView):
    permission_required = 'news.change_post'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    success_url = reverse_lazy('home')


class HomeView(TemplateView):
    template_name = 'index.html'
