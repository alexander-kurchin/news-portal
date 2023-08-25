from django.urls import path
from . import views


urlpatterns = [path('', views.index),
               path('news/', views.PostList.as_view()),
               path('news/<int:pk>', views.PostDetail.as_view()),
               ]
