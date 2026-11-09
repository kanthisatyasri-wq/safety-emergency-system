from django.urls import path
from . import views


urlpatterns = [

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'verify-email/',
        views.verify_email,
        name='verify_email'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'dashboard/',
        views.role_dashboard,
        name='role_dashboard'
    ),

    path(
        'user-dashboard/',
        views.user_dashboard,
        name='user_dashboard'
    ),

    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'superadmin-dashboard/',
        views.superadmin_dashboard,
        name='superadmin_dashboard'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),
    path('', views.home, name='home'),
]