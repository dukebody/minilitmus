from mylitmus.models import Product, Category, Test, Result

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
