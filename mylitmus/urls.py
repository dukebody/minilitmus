#from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from mylitmus.models import Product

urlpatterns = patterns('',
    # Example:
    # (r'^l10ncases/', include('l10ncases.foo.urls')),
    (r'^$', TemplateView.as_view(template_name='mylitmus/front_page.html'), {}, "frontpage" ),
    (r'^help/$', TemplateView.as_view(template_name='mylitmus/help.html'), {}, "help" ),
    (r'^testing/$', ListView.as_view(queryset=Product.objects.filter(active=True)) , {}, "products"),
    (r'^testing/(?P<product_id>\d+)/$', 'mylitmus.views.categories', {}, "categories"),
    (r'^testing/(?P<product_id>\d+)/(?P<category_id>\d+)/$', 'mylitmus.views.tests', ),
    (r'^testing/(?P<product_id>\d+)/version/$', 'mylitmus.views.version', {}, "version" ),
    (r'^admon/copy/(?P<aproductID>\d+)/(?P<bproductID>\d+)/$', 'mylitmus.views.copy', {}, "copy" ),

)
