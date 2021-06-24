from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class News(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField(max_length=1000)
    tags = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)

    objects = models.Manager()

    def __str__(self):
        return f'{self.title}'
