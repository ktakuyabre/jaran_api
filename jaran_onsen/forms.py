from django import forms

from .models import jaranOnsen, jaranOnsenPost

class jaranOnsenForm(forms.ModelForm):
	
	reg = forms.IntegerField(required=False)
	pref = forms.IntegerField(required=False)
	l_area = forms.IntegerField(required=False)
	s_area = forms.IntegerField(required=False)
	onsen_q = forms.IntegerField(required=False)	
	start = forms.IntegerField(required=False)
	count = forms.IntegerField(required=False)	
	xml_pth = forms.IntegerField(required=False)
	class Meta:
		model = jaranOnsenPost
		exclude = ()
		#fields = ('reg', 'pref', 'l_area', 's_area', 'onsen_q', 'start', 'count', 'xml_ptn',) 
