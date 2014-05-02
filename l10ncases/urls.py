from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mylitmus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    (r'^mylitmus/', include('mylitmus.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
