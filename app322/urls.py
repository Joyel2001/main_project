from django.urls import path
from . import views

from .views import all_posts,post_detail,post_comments,login2_page,register_company,signup_view
urlpatterns = [
    path('post_content/', views.post_content, name='post_content'),
    path('all_posts/', all_posts, name='all_posts'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
path('post_comments/<int:post_id>/', post_comments, name='post_comments'),
path('login2_page/', views.login2_page, name='login2_page'),
path('register_company/', register_company, name='register_company'),
 path('signup_view_seller/', signup_view, name='signup_view_seller')

]