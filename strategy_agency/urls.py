"""strategy_agency URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include, re_path


from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework.authtoken import views

schema_view = get_schema_view(
    openapi.Info(
        title= 'Strategy agency',
        default_version='v1',
        description='Swagger docs for Rest API',
    ),
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    path('model-admin/', admin.site.urls), #strategy
    path('', include('new_app.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('drf-auth/', include('rest_framework.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,}),]
urlpatterns += re_path(r'^_nested_admin/', include('nested_admin.urls')),
urlpatterns += [path('api-token-auth/', views.obtain_auth_token)]


admin.site.site_header = "Администрация сайта агентства стратегий"
admin.site.site_title = "Портал администрации агентства стратегии"
admin.site.index_title = "Добро пожаловать на Портал Стратегического агентства"



if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')), 
    ]+urlpatterns