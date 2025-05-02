from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Tags(models.Model):
    tag_name = models.CharField(max_length = 20, unique=True)

    def __str__(self):
        return self.tag_name
    
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF','Draft'
        PUBLISHED = 'PB','Published'

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=250, unique_for_date='publish', unique=True)
    body = models.CharField(max_length = 250)
    status = models.CharField(max_length=2, choices=Status, default=Status.DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    tags = models.ManyToManyField(Tags)




    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse(
            'blog:blog_detail',
            args=[self.publish.year, self.publish.month, self.publish.day, self.slug]
        )
    
class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    email = models.EmailField()
    body = models.CharField(max_length=100)