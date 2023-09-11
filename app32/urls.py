from django.contrib import admin
from django.urls import path
from . import views
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
   
    path('',views.index, name='index'),
    path('loginn',views.loginn,name='loginn'),
    path('register',views.register,name='register'),
    path('loggout',views.loggout,name='loggout'),
    path('check-email-exists/', views.check_email_exists, name='check_email_exists'),
    path('resetpass',views.resetpass,name='resetpass'),
    path('eventbook',views.eventbook,name='eventbook'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    path('user_profile_view', views.user_profile_view, name='user_profile_view'),
    path('addevent/', views.addevent, name='addevent'),
    path('show_events/', views.show_events, name='show_events'),
    path('show_events/<str:category>/', views.show_events, name='show_events_by_category'),  # Add this pattern
    # path('delete_event/', views.delete_event, name='delete_event'),
    path('check-username-exists/', views.check_username_exists, name='check-username-exists'),
    path('event_details_view', views.event_details_view, name='event_details_view'),
    path('edit_event/<str:event_id>/', views.edit_event, name='edit_event'),
    path('delete_event/<str:event_id>/', views.delete_event, name='delete_event'),   # path('enroll/', views.enroll_event, name='enroll_event'),
    
    path('orderforhome', views.orderforhome, name='orderforhome'),
    # urls.py
    path('add_bin/', views.add_bin, name='add_bin'),
    path('add_bin_event/', views.add_bin_event, name='add_bin_event'),
    path('bin_order/', views.bin_order, name='bin_order'),
    path('bin_order_event/', views.bin_order_event, name='bin_order_event'),
     path('admin/app32/bin/<int:object_id>/change/', views.bin_order_event, name='bin_order_event'),
       

    path('registration/confirmation/', views.registration_confirmation, name='registration_confirmation'),
    path('book_event/<str:event_id>/', views.event_booking, name='event_booking'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
        path('hello_admin/', views.hello_admin, name='hello_admin'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('reset_password/', views.reset_password, name='reset_password'),
     path('user-booked-events/', views.user_booked_events, name='user_booked_events'),
     path('bin_details/<int:user_id>/', views.bin_details, name='bin_details'),
     path('user-list/', views.user_list, name='user_list'),
     path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
]

