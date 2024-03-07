from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/',views.login_view, name='login'),
     path('register/', views.register, name='register'),
     path('logout/', views.logout_view, name='logout'),
     path('add/', views.add_blog, name='add_blog'),
     path('edit/<int:blog_id>/', views.edit_blog, name='edit_blog'),
     path('delete/<int:blog_id>/', views.delete_blog, name='delete_blog'),
     path('like/<int:blog_id>/', views.like_blog, name='like_blog'),
      path('add_comment/<int:blog_id>/', views.add_comment, name='add_comment'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)