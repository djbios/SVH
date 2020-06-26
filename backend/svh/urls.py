from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

from svh.views import video_views
from svh.views.api import update_library_cmd, is_superuser
from svh.views.admin import regex_rename_sources, regex_ajax

schema_view = get_swagger_view(title='SVH API')
router = routers.DefaultRouter()
router.register(r'videofolder', video_views.VideoFolderViewSet)
router.register(r'videofile', video_views.VideoFileViewSet)

urlpatterns = [url(r'^updatelibrary/$', update_library_cmd, name='update_library'),
               url(r'^superuser/$', is_superuser, name='superuser'),
               url(r'^admin/rename', regex_rename_sources, name='rename'),
               url(r'^admin/regex', regex_ajax, name='regex'),
               url(r'^swagger/', schema_view),
               path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
               path('', include(router.urls)),
               ]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)