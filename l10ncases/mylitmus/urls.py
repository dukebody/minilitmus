from django.conf.urls.defaults import *
from mylitmus.models import Product

urlpatterns = patterns('',
    # Example:
    # (r'^l10ncases/', include('l10ncases.foo.urls')),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'mylitmus/front_page.html',}, "front-page" ),
    (r'^help/$', 'django.views.generic.simple.direct_to_template', {'template': 'mylitmus/help.html',}, "help" ),
    (r'^testing/$', 'django.views.generic.list_detail.object_list', { 'queryset': Product.objects.filter(active=True) } , "products"),
    (r'^testing/(?P<product_id>\d+)/$', 'mylitmus.views.categories', {}, "categories"),
    (r'^testing/(?P<product_id>\d+)/(?P<category_id>\d+)/$', 'mylitmus.views.tests', ),
    (r'^testing/(?P<product_id>\d+)/version/$', 'mylitmus.views.version', {}, "version" ),
    (r'^admon/copy/(?P<aproductID>\d+)/(?P<bproductID>\d+)/$', 'mylitmus.views.copy', {}, "copy" ),

)
