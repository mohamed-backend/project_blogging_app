from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.post_list_create, name='post-list-create'),
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Where users can post
    path('logout/', views.logout_view, name='logout'),
    path('add_post/', views.add_post, name='add_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),


]
