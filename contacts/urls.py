from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.contacts_list,
        name='contacts_list'
    ),

    path(
        'add/',
        views.add_contact,
        name='add_contact'
    ),

    path(
        'verify/<int:contact_id>/',
        views.verify_contact,
        name='verify_contact'
    ),

    path(
        'delete/<int:contact_id>/',
        views.delete_contact,
        name='delete_contact'
    ),

]
