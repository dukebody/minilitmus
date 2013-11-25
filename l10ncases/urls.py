from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'', include('l10ncases.foo.urls')),
     (r'^qa/', include('mylitmus.urls')),

    # Uncomment this for admin:
     (r'^qa/admin/', include('django.contrib.admin.urls')),
)


handler404 = 'django.views.defaults.page_not_found'
