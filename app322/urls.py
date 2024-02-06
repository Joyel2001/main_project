from django.urls import path
from . import views

from .views import *
urlpatterns = [
path('post_content/', views.post_content, name='post_content'),
path('all_posts/', all_posts, name='all_posts'),
path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
# path('post_comments/<int:post_id>/', post_comments, name='post_comments'),
path('login2_page/', views.login2_page, name='login2_page'),
path('register_company/', register_company, name='register_company'),
path('signup_view_seller/', signup_view, name='signup_view_seller'),
path('forum_index/', forum_index, name='forum_index'),
path('company_login/', company_login, name='company_login'),
path('create_tender/', create_tender, name='create_tender'),
path('tender_list/', tender_list, name='tender_list'),
path('tender/<int:tender_id>/', tender_detail, name='tender_detail'),
path('company_index/', company_index, name='company_index'),
path('seller_login_view/', seller_login_view, name='seller_login_view'),
path('registration/<int:tender_id>/', views.registration_page, name='registration_page'),
 path('companys_profile/', companys_profile, name='companys_profile'),
 path('company_apply_details/', display_company_apply_details, name='company_apply_details'),
]