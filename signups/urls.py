from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

import views

urlpatterns = patterns('',
    url(r'^(.*)/$', views.submit_form, name='email'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)