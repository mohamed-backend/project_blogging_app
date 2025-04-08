from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from blog import views  # Import the view for the homepage

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),  # Blog app API URLs
    path('', views.home, name='home'),  # Homepage
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),  # Logout view
    path('create/', views.create_post, name='create_post'),
    path('edit/<int:id>/', views.edit_post, name='edit_post'),
    path('delete/<int:id>/', views.delete_post, name='delete_post'),
]
