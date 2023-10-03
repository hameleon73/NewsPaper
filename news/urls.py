from django.urls import path
# Импортируем созданное нами представление
from .views import (
   PostList, PostDetail, PostSearch, PostDelete, PostUpdate, PostCreate,
   ArticleDetail, ArticleDelete, ArticleUpdate, ArticleCreate, subscriptions, CategoryListView, subscribe,

)


urlpatterns = [
   path('search/', PostSearch.as_view(), name='post_search'),
   path('news/', PostList.as_view(), name='post_list'),

   path('news/<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

   path('article/<int:pk>', ArticleDetail.as_view(), name='article_detail'),
   path('article/create/', ArticleCreate.as_view(), name='article_create'),
   path('article/<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
   path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),

   path('subscriptions/', subscriptions, name='subscriptions'),

   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

#   path('', IndexView.as_view()),
]