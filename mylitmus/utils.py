import re
from mylitmus.models import Product, Category, Test, Result
from config import LANGCODES

# copy aproduct categories and tests to bproduct
def copy_product_data(aproduct, bproduct):
	acategories = Category.objects.filter(productID=aproduct)
	# copy categories from a to b
	for acategory in acategories:
		bcategory = Category(productID=bproduct, name=acategory.name, description=acategory.description)
		bcategory.save()
		# and copy tests in each category
		atests = Test.objects.filter(categoryID=acategory)
		for atest in atests:
			btest = Test(categoryID=bcategory, name=atest.name, description=atest.description)
			btest.save()


def getVersion(request, product_id, guess=False):
	localekey = 'version-' + str(product_id) + '-locale'
	oskey = 'version-' + str(product_id) + '-os'
	buildIDkey = 'version-' + str(product_id) + '-buildID'

	try:
		version = {
			'locale': request.session[localekey], 
			'os': request.session[oskey], 
			'buildID': request.session[buildIDkey]
			}
	except KeyError:
		version = {}

	if version:
		return version


	if guess:
		try:
			langtoken = request.META['HTTP_ACCEPT_LANGUAGE'].split(',')[0].split(';')[0]
		except KeyError:
			langtoken = ''
		version['locale'] = LANGCODES.get(langtoken, 'es-ES')

		
		useragent = request.META['HTTP_USER_AGENT']

		if useragent.find("Linux") != 1:
			os = "linux"
		elif useragent.find("Mac") != 1:
			os = "mac"
		else:
			os = "windows"
		version['os'] = os


		buildID_re = re.search(r'Gecko/(\d+)', useragent)
		if buildID_re:
			buildID = buildID_re.groups()[0]
		else:
			buildID = ''
		version['buildID'] = buildID

	return version