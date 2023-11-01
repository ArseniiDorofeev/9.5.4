from datetime import timezone

from django.contrib.auth.models import User
from django.db import models
from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    objects = None
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = 3 * sum(
            post.rating for post in Post.objects.filter(author=self))
        comment_rating = sum(comment.rating for comment in Comment.objects.filter(
            user=self.user))
        self.rating = post_rating + comment_rating
        self.save()


class Category(models.Model):
    objects = None
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    objects = None
    POST_TYPES = [
        ('article', 'Статья'),
        ('news', 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    objects = None
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class News:
    pass


class Article:
    pass


class UserProfile:
    pass


from django.contrib.auth.models import Group


def create_groups():
    Group.objects.get_or_create(name='common')
    Group.objects.get_or_create(name='authors')


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        create_groups()


from django.db import models
from django.contrib.auth.models import User


class AuthorRequest(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    requested_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_create = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subscribers = models.ManyToManyField(User, related_name='subscribed_posts', blank=True)


class Appointment:
    pass


class Subscriber:
    pass