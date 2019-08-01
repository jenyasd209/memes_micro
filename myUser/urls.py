from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name = 'profile'),
    path('logout/', views.logout_view, name= 'logout_view'),
    path('new_post/', views.new_post, name= 'new_post'),
    path('edit/', views.edit_profile, name= 'edit_profile'),
    # path('delete_post/<int:id_post>/', views.delete_post, name = 'delete_post'),
]
