from django.urls import path
from . import views

urlpatterns = [
    path('users', views.users, name = 'users'),
    path('delete_user_<int:id_user>', views.delete_user, name = 'delete_user'),
    path('categories', views.categories, name = 'categories'),
    path('add_category', views.add_category, name = 'add_category'),
    path('search_user', views.search_user, name = 'search_user'),
    path('delete_category_<int:id_category>', views.delete_category, name = 'delete_category'),

    path('backup', views.backup, name = 'backup'),
    path('export', views.export, name = 'export'),
]
