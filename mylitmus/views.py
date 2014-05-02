from mylitmus.models import Product, Category, Test, Result
from mylitmus.forms import ResultForm, VersionForm, VersionFormCaptcha
from mylitmus.utils import copy_product_data, getVersion

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test


# Create your views here.


def categories(request, product_id):
	product = get_object_or_404(Product, pk=product_id, active=True)
	categs = Category.objects.filter(productID=product_id)  

	version = getVersion(request, product_id)
	if not version:
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
	
	return render_to_response('mylitmus/category_list.html', {'categs':categs, 'product':product,'locale':version['locale'], 'os':version['os'], 'buildID':version['buildID']}, context_instance=RequestContext(request))
	
def tests(request, product_id, category_id):
	tests = Test.objects.filter(categoryID=category_id, categoryID__productID=product_id)  # set of tests for this category 
	if not tests:  # not valid (product, category) pair
		raise Http404

	product = get_object_or_404(Product, pk=product_id, active=True)
	category = Category.objects.get(pk=category_id)

	version = getVersion(request, product_id)
	if not version:
		return HttpResponseRedirect(reverse('version', args=[product.id]))

	# validate cookie data
	cookieForm = VersionForm({'locale':version['locale'], 'os':version['os'], 'buildID':version['buildID']})
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
					r = Result(testID=test, passed=passed, comments=comments, locale=version['locale'], os=version['os'], buildID=version['buildID'])
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

	return render_to_response('mylitmus/test_list.html', {'tests':tests, 'resultforms':resultforms, 'product':product, 'category':category, 'locale':version['locale'], 'os':version['os'], 'buildID':version['buildID']},context_instance=RequestContext(request))

def version(request, product_id):
	product = get_object_or_404(Product, pk=product_id, active=True)

	localekey = 'version-' + str(product_id) + '-locale'
	oskey = 'version-' + str(product_id) + '-os'
	buildIDkey = 'version-' + str(product_id) + '-buildID'

	version = getVersion(request, product_id, guess=True)

	if request.method == 'POST':
		postdata = request.POST
		f = VersionFormCaptcha(postdata)
		if f.is_valid():
			request.session[localekey] = f.cleaned_data['locale']
			request.session[oskey] = f.cleaned_data['os']
			request.session[buildIDkey] = f.cleaned_data['buildID']

			return HttpResponseRedirect(product.get_absolute_url())

	else:
		f = VersionFormCaptcha(initial=version)

	return render_to_response( 'mylitmus/version.html', {'form':f, 'product':product, 'locale':version['locale'], 'os':version['os'], 'buildID':version['buildID'], }, context_instance=RequestContext(request) )


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

