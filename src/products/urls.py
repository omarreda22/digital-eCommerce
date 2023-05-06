from django.urls import path

from . import views

app_name = "products"


urlpatterns = [
    path('', views.product_list, name="product-list"),
    path('create/', views.product_create, name='create'),
    path('<slug:handle>/', views.product_detail, name='details'),
    path('<slug:handle>/manager/', views.product_manager, name='manager'),
    path('<slug:handle>/download/<int:pk>', views.product_images_download, name='download')
]
