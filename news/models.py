from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    def update_rating(self): #взял данный блок из разбора, т.к. своя конструкция получалась не очень. про aggregate не знал
        postRat = self.post_set.aggregate(postRating=Sum('post_rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.author_user.comment_set.aggregate(commentRating=Sum('comment_rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.author_rating = pRat * 3 + cRat
        self.save()

    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)


class Category(models.Model):
    cat_name = models.CharField(max_length=50, unique=True)


class Post(models.Model):
    def like(self):
        self.post_rating += 1
        self.save()
    def dislike(self):
        self.post_rating -= 1
        self.save()
    def preview(self):
        return self.post_title[0:123]+'...'

    news = 'NW'
    post = 'PS'
    CAT_TYPES = [(news, 'Новость'),
                 (post, 'Статья')]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    cat_type = models.CharField(max_length=2, choices=CAT_TYPES, default=post)
    time_in = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    def like(self):
        self.comment_rating += 1
        self.save()
    def dislike(self):
        self.comment_rating -= 1
        self.save()

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

