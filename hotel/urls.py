from django.urls import path
from . import views

urlpatterns = [
    path('insert-data/', views.insert_hotel_data, name='insert_hotel_data'),
    path('show-all/', views.show_all_data, name='show_all_data' ),
    path('show-all-drf/', views.show_all_by_drf, name='show_all_by_drf'),
    path('show-all-drf-page/', views.show_all_drf_by_page, name='show_all_drf_by_page'),
    path('post-data/', views.post_data_by_drf, name='post_data_by_drf'),
    path('details/<int:id>', views.hotel_details, name='hotel_details')
]
