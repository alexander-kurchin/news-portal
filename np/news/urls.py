from django.urls import path
from . import views


urlpatterns = [path('', views.index, name='home'),
               path('news/', views.PostList.as_view(),
                    {'post_type': 'news'}, name='news_list'),
               path('news/create', views.PostCreate.as_view(),
                    {'post_type': 'news'}, name='news_create'),
               path('news/search', views.PostFilter.as_view(),
                    {'post_type': 'news'}, name='news_filter'),

               path('articles/', views.PostList.as_view(),
                    {'post_type': 'article'}, name='articles_list'),
               path('articles/create', views.PostCreate.as_view(),
                    {'post_type': 'article'}, name='article_create'),

               path('post_<int:pk>', views.PostDetail.as_view(), name='post_detail'),
               path('post_<int:pk>/edit', views.PostUpdate.as_view(), name='post_edit'),
               path('post_<int:pk>/delete', views.PostDelete.as_view(), name='post_delete'),

               # На случай тестов
               path('news/<int:pk>', views.PostDetail.as_view()),
               path('news/<int:pk>/edit', views.PostUpdate.as_view()),
               path('news/<int:pk>/delete', views.PostDelete.as_view()),

               path('articles/<int:pk>', views.PostDetail.as_view()),
               path('articles/<int:pk>/edit', views.PostUpdate.as_view()),
               path('articles/<int:pk>/delete', views.PostDelete.as_view()),
               ]
