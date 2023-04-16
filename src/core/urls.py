from django.conf import settings
from django.contrib import admin
from django.urls import path

from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view)
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns +=  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)