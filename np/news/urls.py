from django.urls import path
from django.views.decorators.cache import cache_page

from . import views


urlpatterns = [path('', cache_page(60*5)(views.HomeView.as_view()), name='home'),

               path('news/', cache_page(60*1)(views.PostList.as_view()),
                    {'post_type': 'news'}, name='news_list'),
               path('news/create', views.PostCreate.as_view(),
                    {'post_type': 'news'}, name='news_create'),
               path('news/search', views.PostFilter.as_view(),
                    {'post_type': 'news'}, name='news_filter'),

               path('articles/', cache_page(60*1)(views.PostList.as_view()),
                    {'post_type': 'article'}, name='articles_list'),
               path('articles/create', views.PostCreate.as_view(),
                    {'post_type': 'article'}, name='article_create'),

               path('post_<int:pk>', views.PostDetail.as_view(), name='post_detail'),
               path('post_<int:pk>/edit', views.PostUpdate.as_view(), name='post_edit'),
               path('post_<int:pk>/delete', views.PostDelete.as_view(), name='post_delete'),

               path('categories/', cache_page(60*5)(views.CategoryList.as_view()), name='all_categories'),
               path('category_<int:pk>', cache_page(60*5)(views.PostCategoryList.as_view()), name='category'),
               path('category_<int:pk>/subscribe', views.CategorySubscribe.as_view(), name='subscribe'),
               ]
