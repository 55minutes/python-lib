from django.conf.urls.defaults import *

urlpatterns = patterns('fiftyfive.apps.imageview.views',
        (r'^image/(\S+)/$', 'imageview.showMedium'),
        (r'^gallery/$', 'imageview.gallery'),
        (r'^.*$', 'imageview.index'),
        )
