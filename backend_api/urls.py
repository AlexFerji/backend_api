from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.routers import SimpleRouter
from rest_framework import permissions

from post_image.views import ImageList



schema_view = get_schema_view(
    openapi.Info(
        title="Model API",
        default_version="v1",
        description="Сайт для загрузки изображений",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="hello@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


router = SimpleRouter()
router.register('image_list', ImageList, basename='ImageList')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api-auth/', include('rest_framework.urls')),
    path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api/v1/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/v1/', include('post_image.urls')),
    path('api/', include(router.urls)),
    path('swagger', schema_view.with_ui( 'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc', schema_view.with_ui( 'redoc', cache_timeout=0), name='schema-redoc')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)