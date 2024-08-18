from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('signup_success/', views.signup_success, name='signup_success'),
    path('unapproved_users/', views.InactiveUserListView.as_view(), name='unapproved_users'),
    path('approve_users/', views.ApproveUsersView.as_view(), name='approve_users'),
]