from django.urls import path

from . import views

app_name = 'orders'


urlpatterns = [
    path('start/', views.orders_process_start, name='order_start'),
    path('success/', views.orders_process_success, name='order_success'),
    path('error/', views.orders_process_error, name='order_error'),
]
