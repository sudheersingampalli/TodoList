from django import forms
from .models import Todomodel

class Todoform(forms.ModelForm):
	class Meta:
		model = Todomodel
		fields = ['date','description','status']
