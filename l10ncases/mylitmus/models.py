#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import permalink

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length=30)
	version = models.CharField(max_length=10)
	description = models.TextField()
	downloadlink = models.URLField()
	logo = models.ImageField(upload_to="logos/")
	active = models.BooleanField()

	def __unicode__(self):
		return u'%s %s' % (self.name, self.version)
	
	class Admin:
		pass

	def get_absolute_url(self):
		return ('mylitmus.views.categories', [str(self.id)])
	get_absolute_url= permalink(get_absolute_url)

class Category(models.Model):
	productID = models.ForeignKey(Product)
	name = models.CharField(max_length=30)
	description = models.TextField()

	def __unicode__(self):
		return u'%s :: %s' % (self.productID, self.name)
	
	class Admin:
		pass

	def get_absolute_url(self):
		return ('mylitmus.views.tests', [str(self.id)])
	get_absolute_url= permalink(get_absolute_url)

class Test(models.Model):
	categoryID = models.ForeignKey(Category, 
			edit_inline=models.STACKED, min_num_in_admin=1, num_extra_on_change=3)
	name = models.CharField(max_length=30, core=True)
	description = models.TextField(core=True)

	def __unicode__(self):
		return u'%s :: %s' % (self.categoryID, self.name)
	
	class Admin:
		pass

class Result(models.Model):
	PASSED_CHOICES = (
			('n', 'No realizado'),
			('t', 'Correcto'),
			('f', 'Fallido'),
	)


	OSES = (
			('windows', 'Windows'),
			('mac', 'Mac'),
			('linux', 'Linux'),
	)

	LOCALES = (
			('es-AR', 'Español de Argentina'),
			('es-BO', 'Español de Bolivia'),
			('es-CL', 'Español de Chile'),
			('es-CO', 'Español de Colombia'),
			('es-ES', 'Español de España'),
			('es-MX', 'Español de México'),
			('es-PE', 'Español de Perú'),
	)

	testID = models.ForeignKey(Test)
	date = models.DateTimeField(auto_now_add=True,)
	passed = models.CharField(max_length=1, choices=PASSED_CHOICES, default='n')
	comments = models.TextField(blank=True)
	os = models.CharField(max_length=10, choices=OSES, default='windows')
	buildID = models.IntegerField()
	locale = models.CharField(max_length=5, choices=LOCALES, default='es-ES')

	def __unicode__(self):
		return u'%s, %s' % (self.testID, self.passed)
			
	class Admin:
		list_display = ('testID', 'locale', 'passed', 'comments')
		list_filter = ('testID', 'passed', 'locale', )

