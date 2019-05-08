from django import forms

from .models import jaranOnsen, jaranOnsenPost

class jaranOnsenForm(forms.ModelForm):
	
	class Meta:
		model = jaranOnsenPost
		#fields = ('reg', 'pref', 'l_area', 's_area', 'onsen_q', 'start', 'count', 'xml_ptn',) 
		fields = ('l_area', 'count', 'xml_ptn',)
