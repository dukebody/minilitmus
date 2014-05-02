#!/usr/bin/python
# -*- coding: utf-8 -*-

from django import forms
from mylitmus.models import Result
from mylitmus.widgets import RadioFieldRendererPassed
import re
from random import randint

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

class ResultForm(forms.Form):
	PASSED_CHOICES = (
			('n', 'No realizado'),
			('t', 'Correcto'),
			('f', 'Fallido'),
	)

	passed = forms.ChoiceField(choices=PASSED_CHOICES, initial='n', 
			widget=forms.RadioSelect(renderer=RadioFieldRendererPassed))
	comments = forms.CharField(widget=forms.Textarea(), required=False)

	def clean(self):
		"""
		If the test failed, the user should indicate why (4 letters or more)
		"""
		if self.is_valid():
			if self.cleaned_data['passed'] == 'f' and len(self.cleaned_data['comments']) < 4:
				raise forms.ValidationError('Por favor, indica por qué falló la prueba')
			else:
				return self.cleaned_data

class VersionForm(forms.Form):
	locale = forms.ChoiceField(choices=LOCALES)
	os = forms.ChoiceField(choices=OSES)
	buildID = forms.IntegerField(error_messages={'required':'Este campo es obligatorio', 'invalid':'Introduce un número'})

class VersionFormCaptcha(VersionForm):
	Q_RE = re.compile("^(\d)\+(\d)$")
	A_RE = re.compile("^(\d+)$")
	captcha_question = forms.CharField(max_length=10, required=True, 
        	widget=forms.HiddenInput())
	captcha_answer = forms.CharField(max_length = 2, required=True, 
			error_messages={'required':'Escribe el resultado de la suma'}, widget = forms.TextInput(attrs={'size':'2'}))

    	def __init__(self, *args, **kwargs):
        	super(VersionForm, self).__init__(*args, **kwargs)
	        q = self.data.get('captcha_question') or self._generate_question()
        	self.initial['captcha_question'] = q

	def _generate_question(self):
        	return "%s+%s" % (randint(1,9), randint(1,9))

	def clean_captcha_answer(self):
        	q = self.Q_RE.match(self.cleaned_data['captcha_question'])
	        if not q:
        		raise forms.ValidationError("¿Te crees un hacker?")
	        q = q.groups()
        	a = self.A_RE.match(self.cleaned_data['captcha_answer'])
	        if not a:
        	    raise forms.ValidationError("Escribe el resultado de la suma")
	        a = a.groups()
        	if int(q[0]) + int(q[1]) != int(a[0]):
			raise forms.ValidationError("El resultado es incorrecto; usa tus dedos si es preciso")


class MathCaptchaForm(forms.Form):
    Q_RE = re.compile("^(\d)\+(\d)$")
    A_RE = re.compile("^(\d+)$")
    captcha_question = forms.CharField(max_length=10, required=True,
        widget=forms.HiddenInput())
    captcha_answer = forms.CharField(max_length = 2, required=True,
        widget = forms.TextInput(attrs={'size':'2'}))

    def __init__(self, *args, **kwargs):
        super(MathCaptchaForm, self).__init__(*args, **kwargs)
        q = self.data.get('captcha_question') or self._generate_question()
        self.initial['captcha_question'] = q

    def _generate_question(self):
        return "%s+%s" % (randint(1,9), randint(1,9))

    def clean_captcha_answer(self):
        q = self.Q_RE.match(self.cleaned_data['captcha_question'])
        if not q:
            raise forms.ValidationError("Are you hacker?")
        q = q.groups()
        a = self.A_RE.match(self.cleaned_data['captcha_answer'])
        if not a:
            raise forms.ValidationError("Number is expected!")
        a = a.groups()
        if int(q[0]) + int(q[1]) != int(a[0]):
            raise forms.ValidationError("Are you human?")

