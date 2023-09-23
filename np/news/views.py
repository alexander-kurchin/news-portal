from django.contrib.auth.mixins import (LoginRequiredMixin,
                                        PermissionRequiredMixin)
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, FormView,
                                  ListView, TemplateView, UpdateView)
from django_filters.views import FilterView

from .filters import PostFilterSet
from .forms import PostForm
from .models import Author, Category, CategoryUser, Post, PostCategory, User


class HomeView(TemplateView):
    template_name = 'index.html'


class PostList(ListView):
    model = Post
    paginate_by = 10

    # TODO: Может быть правильнее переопределить def get_queryset()
    def get(self, request, *args, **kwargs):
        post_type = kwargs['post_type']
        self.queryset = Post.objects.filter(post_type=post_type)
        return super(PostList, self).get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


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


class CategoryList(ListView):
    model = Category


# TODO: Может быть сделать через (SingleObjectMixin, ListView)
class PostCategoryList(ListView):
    model = PostCategory
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.queryset = PostCategory.objects.filter(category=kwargs['pk']).distinct()
        self.category_pk = kwargs['pk']
        return super(PostCategoryList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.category_pk)
        return context


class CategorySubscribe(LoginRequiredMixin, TemplateView):
    template_name = 'news/category_subscribe.html'

    def get(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=kwargs['pk'])
        self.user = get_object_or_404(User, username=request.user.username)
        return super(CategorySubscribe, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = not CategoryUser.objects.filter(category=self.category, user=self.user).exists()
        context['user_has_email'] = self.request.user.email
        context['category'] = self.category
        return context

    def post(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=kwargs['pk'])
        self.user = get_object_or_404(User, username=request.user.username)
        CategoryUser.objects.get_or_create(category=self.category, user=self.user)
        return redirect('subscribe', pk=self.category.pk)
