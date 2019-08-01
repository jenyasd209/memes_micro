from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id_user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar_url = models.CharField(max_length=150, default='image/default_avatar.png')
    birthday = models.DateField(null = True)
    gender = models.CharField(max_length=2, default='М', null = True)
    count_comment = models.IntegerField(default = 0)
    count_post = models.IntegerField(default = 0)

    def __str__(self):
        return self.avatar_url

# Create your models here.
