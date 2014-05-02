#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import permalink
from django.core.urlresolvers import reverse

from config import OSES, LOCALES, PASSED_CHOICES


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
    
    def get_absolute_url(self):
        return reverse('mylitmus.views.categories', args=[str(self.id)])


class Category(models.Model):
    productID = models.ForeignKey(Product)
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __unicode__(self):
        return u'%s :: %s' % (self.productID, self.name)

    def get_absolute_url(self):
        return reverse('mylitmus.views.tests', args=[str(self.id)])


class Test(models.Model):
    categoryID = models.ForeignKey(Category)
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __unicode__(self):
        return u'%s :: %s' % (self.categoryID, self.name)


class Result(models.Model):
    testID = models.ForeignKey(Test)
    date = models.DateTimeField(auto_now_add=True,)
    passed = models.CharField(max_length=1, choices=PASSED_CHOICES, default='n')
    comments = models.TextField(blank=True)
    os = models.CharField(max_length=10, choices=OSES, default='windows')
    buildID = models.IntegerField()
    locale = models.CharField(max_length=5, choices=LOCALES, default='es-ES')

    def __unicode__(self):
        return u'%s, %s' % (self.testID, self.passed)
