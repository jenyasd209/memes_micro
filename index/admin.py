from django.contrib import admin
from .models import Category, Post, Comments

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comments)

# Register your models here.
