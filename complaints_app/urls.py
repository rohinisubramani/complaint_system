from django.urls import path
from . import views

urlpatterns = [
    # Public & Student Authentication
    path('', views.home, name='home'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    # Student Dashboard & Complaints
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('submit-complaint/', views.submit_complaint, name='submit_complaint'),
    path('my-complaints/', views.my_complaints, name='my_complaints'),
    path('complaint/<str:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('complaint/<str:complaint_id>/delete/', views.delete_complaint, name='delete_complaint'),
    path('profile/', views.user_profile, name='user_profile'),

    # Admin Interfaces
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-complaints/', views.admin_complaints, name='admin_complaints'),
    path('admin-complaints/<str:complaint_id>/update/', views.admin_update_complaint, name='admin_update_complaint'),
    path('admin-complaints/<str:complaint_id>/delete/', views.admin_delete_complaint, name='admin_delete_complaint'),
    path('admin-users/', views.admin_users, name='admin_users'),
]
