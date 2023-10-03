from celery import shared_task
import datetime
from .models import Post, Category, PostCategory
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

@shared_task
def everyweek_notifications():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_in__gte=last_week)
    categories = set(posts.values_list('categories__cat_name', flat=True))
    subscribers = set(Category.objects.filter(cat_name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'daily_post.html',
        {
            'link': 'http://127.0.0.1:8000',
            'posts': posts,

        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@shared_task()
def send_notifications(preview, pk, post_title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=post_title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()

#@receiver(m2m_changed, sender=PostCategory)
#def notify_about_new_post(instance, sender, **kwargs):
#    if kwargs['action'] =='post_add':
#        categories = instance.categories.all()
#        subscribers: list[str] = []
#        for category in categories:
#            subscribers += category.subscribers.all()

#        subscribers = [s.email for s in subscribers]

#       send_notifications(instance.preview(), instance.pk, instance.post_title, subscribers)