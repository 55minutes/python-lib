from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('',
    (r'^thebook/admin/', include('django.contrib.admin.urls.admin')),
    (r'^thebook/', include('fiftyfive.apps.imageview.settings.urls.main')),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
