#!/usr/bin/python
# -*- coding: utf-8 -*-

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

# maps HTTP_ACCEPT_LANGUAGE to ISO lang codes
LANGCODES = {
    'es-ar':'es-AR', 
    'es-bo':'es-BO', 
    'es-cl':'es-CL', 
    'es-co':'es-CO', 
    'es-es':'es-ES', 
    'es-mx':'es-MX',
    'es-pe':'es-PE',}