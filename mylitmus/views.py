from mylitmus.models import Product, Category, Test, Result
from mylitmus.forms import ResultForm, VersionForm, VersionFormCaptcha
from mylitmus.utils import copy_product_data
#from django.views.generic.list_detail import object_list, object_detail
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
import re

# Create your views here.


def categories(request, product_id):
	product = get_object_or_404(Product, pk=product_id, active=True)
	categs = Category.objects.filter(productID=product_id)  


	localekey = 'version-' + str(product.id) + '-locale'
	oskey = 'version-' + str(product.id) + '-os'
	buildIDkey = 'version-' + str(product.id) + '-buildID'

	# Check if user has already entered version info
	try:
		locale = request.session[localekey]
		os = request.session[oskey]
		buildID = request.session[buildIDkey]
	except KeyError:
		return HttpResponseRedirect(reverse('version', args=[product.id]))
	
	for categ in categs:
		ts = Test.objects.filter(categoryID=categ.id)  # total tests
		tt = [ x.testID.id for x in Result.objects.all() ]  # tests done IDs
		tds = ts.filter(id__in=tt) # performed tests
		try:
			categ.covered = str(float(len(tds))/len(ts)*100)
		except ZeroDivisionError:
			categ.covered = 0

		categ.alreadytested = request.session.get('alreadytested-'+str(categ.id), False)
	
	return render_to_response('mylitmus/category_list.html', {'categs':categs, 'product':product,'locale':locale, 'os':os, 'buildID':buildID}, context_instance=RequestContext(request))
	
def tests(request, product_id, category_id):
	tests = Test.objects.filter(categoryID=category_id, categoryID__productID=product_id)  # set of tests for this category 
	if not tests:  # not valid (product, category) pair
		raise Http404

	product = get_object_or_404(Product, pk=product_id, active=True)
	category = Category.objects.get(pk=category_id)

	# Check if user has already entered version info
	localekey = 'version-' + str(product.id) + '-locale'
	oskey = 'version-' + str(product.id) + '-os'
	buildIDkey = 'version-' + str(product.id) + '-buildID'

	try:
		locale = request.session[localekey]
		os = request.session[oskey]
		buildID = request.session[buildIDkey]
	except KeyError:
		return HttpResponseRedirect(reverse('version', args=[product.id]))

	# validate cookie data
	cookieForm = VersionForm({'locale':locale, 'os':os, 'buildID':buildID})
	if not cookieForm.is_valid():
		return HttpResponseRedirect(reverse('version', args=[product.id]))

	resultforms = []
	onefilled = False
	allvalid = True


	if request.method == 'POST':
		postdata = request.POST
		for test in tests:
	
			if postdata.get((str(test.id) + '-passed'), '') == 't' or \
				postdata.get((str(test.id) + '-passed'), '') == 'f':
				filled = True

			else:
				filled = False

			passed = postdata.get((str(test.id)+ '-passed'))
			comments = postdata.get(str(test.id) + '-comments', '')

			f = ResultForm({str(test.id) + '-comments':comments,
				str(test.id) + '-passed':passed},
				prefix=test.id )
			f.testlabel = test.description
			resultforms.append(f)

			if filled:
				onefilled = True  # at least one result filled up
				if f.is_valid():
					passed = f.cleaned_data['passed']
					comments = f.cleaned_data['comments']
					r = Result(testID=test, passed=passed, comments=comments, locale=locale, os=os, buildID=buildID)
					r.save()
				else:
					allvalid = False
			
		# the user will be taken to the product page if no form is filled
		if not onefilled:
			return HttpResponseRedirect(product.get_absolute_url())

		if allvalid:
			request.session['alreadytested-' + category_id]=True
			request.session['alreadyhelped'] = True
			return HttpResponseRedirect(product.get_absolute_url())	

	else:
		for test in tests:
			f = ResultForm(prefix=test.id)
			f.testlabel = test.description
			resultforms.append(f)

	return render_to_response('mylitmus/test_list.html', {'tests':tests, 'resultforms':resultforms, 'product':product, 'category':category, 'locale':locale, 'os':os, 'buildID':buildID},context_instance=RequestContext(request))

def version(request, product_id):
	product = get_object_or_404(Product, pk=product_id, active=True)


	localekey = 'version-' + str(product.id) + '-locale'
	oskey = 'version-' + str(product.id) + '-os'
	buildIDkey = 'version-' + str(product.id) + '-buildID'

	# maps HTTP_ACCEPT_LANGUAGE to ISO lang codes
	langcodes = {'es-ar':'es-AR', 'es-bo':'es-BO', 'es-cl':'es-CL', 'es-co':'es-CO', 'es-es':'es-ES', 'es-mx':'es-MX','es-pe':'es-PE',}
	useragent = request.META['HTTP_USER_AGENT']

	try:
		locale = request.session[localekey]
	except KeyError:
		try:
			langtoken = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[0].split(';')[0]
		except KeyError:
			langtoken = ''
		locale = langcodes.get(langtoken, 'es-ES')

	try:
		os = request.session[oskey]
	except KeyError:
		if useragent.find("Linux") != 1:
			os = "linux"
		elif useragent.find("Mac") != 1:
			os = "mac"
		else:
			os = "windows"

	try:
		buildID = request.session[buildIDkey]
	except KeyError:
		buildID_re = re.search(r'Gecko/(\d+)', useragent)
		if buildID_re:
			buildID = buildID_re.groups()[0]
		else:
			buildID = ''


	if request.method == 'POST':
		postdata = request.POST
		f = VersionFormCaptcha(postdata)
		if f.is_valid():
			request.session[localekey] = f.cleaned_data['locale']
			request.session[oskey] = f.cleaned_data['os']
			request.session[buildIDkey] = f.cleaned_data['buildID']

			return HttpResponseRedirect(product.get_absolute_url())

	else:
		f = VersionFormCaptcha(initial={'locale':locale, 'os':os, 'buildID':buildID,})

	return render_to_response( 'mylitmus/version.html', {'form':f, 'product':product, 'locale':locale, 'os':os, 'buildID':buildID, }, context_instance=RequestContext(request) )


# the user can add categories and tests
def user_can_copy(user):
		return user.has_perm("mylitmus.add_category") and user.has_perm("mylitmus.add_test")


@staff_member_required
@user_passes_test(user_can_copy)
def copy(request, aproductID, bproductID):
	aproduct = get_object_or_404(Product, id=aproductID)
	bproduct = get_object_or_404(Product, id=bproductID)

	copy_product_data(aproduct, bproduct)

	return HttpResponseRedirect(bproduct.get_absolute_url())

