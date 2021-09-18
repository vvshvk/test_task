from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('image/', views.upload_img, name='image'),
    path('result/', views.count_hex, name='count_hex')
   ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
