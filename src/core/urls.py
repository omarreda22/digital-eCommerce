from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view),
    path('products/', include('products.urls', namespace='products'))
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)