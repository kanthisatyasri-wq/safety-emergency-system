from django.urls import path
from . import views

urlpatterns = [
    path('sos/', views.sos, name='sos'),

    path(
        'accident/',
        views.sos,
        {'emergency_type': 'ACCIDENT'},
        name='accident_report'
    ),

    path(
        'sos/success/<int:emergency_id>/',
        views.sos_success,
        name='sos_success'
    ),

    path(
        'resolve/<int:emergency_id>/',
        views.resolve_emergency,
        name='resolve_emergency'
    ),

    path(
        'accept-email/<str:token>/',
        views.accept_emergency_email,
        name='accept_emergency_email'
    ),
    path(
    'history/',
    views.emergency_history,
    name='emergency_history'
),
path(
    'statistics/',
    views.emergency_statistics,
    name='emergency_statistics'
),
]