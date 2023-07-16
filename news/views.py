from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, UpdateView, DeleteView, CreateView)
from .models import Post, Category
from datetime import datetime
from .filters import PostFilter
from .forms import PostForm, ArticleForm

from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from tasks import notify_about_new_post

from .tasks import hello


class PostList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'news.html'
    context_object_name = 'post'
    paginate_by = 10
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'post'

class ArticleDetail(DetailView):
    model = Post
    template_name = 'article.html'
    context_object_name = 'post'

class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post'
    paginate_by = 20
    # Переопределяем функцию получения списка
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context['filterset'] = self.filterset
       return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.cat_type = 'NW'
        notify_about_new_post.apply_async([post.pk])
        return super().form_valid(form)

class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.cat_type = 'PS'
        notify_about_new_post.apply_async([post.pk])
        return super().form_valid(form)

class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'

class ArticleUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = ArticleForm
    model = Post
    template_name = 'article_edit.html'

class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('cat_name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context
@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = "Вы подписались на новости категории"
    return render(request, 'subscribe.html', {'category': category, 'message': message})


