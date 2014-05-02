from django.forms.widgets import RadioFieldRenderer, RadioInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


class RadioFieldRendererPassed(RadioFieldRenderer):
	def __iter__(self):
	        for i, choice in enumerate(self.choices):
        		yield RadioInputFormatted(self.name, self.value, self.attrs.copy(), choice, i)

	def __getitem__(self, idx):
        	choice = self.choices[idx] # Let the IndexError propogate
	        return RadioInputFormatted(self.name, self.value, self.attrs.copy(), choice, idx)
	def render(self):
        	"""Outputs a <ul> for this set of radio fields."""
	        return mark_safe(u'<ul class="passed_choices">\n%s\n</ul>' % u'\n'.join([u'<li class="passed_choices">%s</li>'
        	        % force_unicode(w) for w in self]))

class RadioInputFormatted(RadioInput):
	def __unicode__(self):
		return mark_safe(u'<label class="%s">%s %s</label>' % (self.choice_value, self.tag(),
        	        conditional_escape(force_unicode(self.choice_label))))
