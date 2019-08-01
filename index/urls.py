from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('old', views.old, name = 'old'),
    path('user_id<int:id_user>', views.profile_user, name = 'profile_user'),
    path('post_id<int:id_post>/new_comment/', views.new_comment, name= 'new_comment'),
    path('c_<category>/', views.category, name = 'category'),
    path('post_id<int:id_post>/', views.post, name = 'post'),
    path('edit_post/<int:id_post>/', views.edit_post, name = 'edit_post'),
    path('delete_post/<int:id_post>/', views.delete_post, name = 'delete_post'),
    path('delete_comment/<int:id_comment>/', views.delete_comment, name = 'delete_comment'),
]
