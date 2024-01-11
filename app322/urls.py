from django.urls import path
from . import views
from .views import all_posts,post_detail
urlpatterns = [
    path('post_content/', views.post_content, name='post_content'),
    path('all_posts/', all_posts, name='all_posts'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
]