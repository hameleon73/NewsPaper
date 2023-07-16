from django.apps import AppConfig
import redis

class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        from . import signals

red = redis.Redis(
    host='redis-11415.c246.us-east-1-4.ec2.cloud.redislabs.com',
    port=11415,
    password='FWRLkYYt8iUMhZUIYIrf2maYOSXBaRrB'
)