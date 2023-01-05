from django.contrib import admin
from django.urls import path
from .views import UploadImage
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/', UploadImage.as_view(), name='upload'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
