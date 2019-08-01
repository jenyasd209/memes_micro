from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name_category = models.CharField(max_length=150)

    def __str__(self):
        return self.name_category

class Post(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    image_url = models.CharField(max_length=150, null = True)
    published_date = models.DateTimeField(auto_now_add = True)
    count_comment = models.IntegerField(default = 0)

    def __str__(self):
        return self.id

class Comments(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.id)
# Create your models here.
