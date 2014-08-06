from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from users import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^signup/$', views.new_user, name='new_user'),
    url(r'^login/$', views.user_login, name='u_login'),
    url(r'^browse/$', views.browse, name='browse'),
    url(r'^pt/$', views.personal_trainer, name='pt'),
    url(r'^(?P<username>\w+)/$', views.detail, name='detail'),
    url(r'^(?P<username>\w+)/account/$', views.account, name='account'),
    url(r'^logout/$', views.user_logout, name='u_logout'),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)