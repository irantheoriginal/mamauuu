from django import forms

from . import models

class FazerpropostaForm(forms.ModelForm):

class Meta:
	model = models.Fazerproposta
	fields = ('question', 'choice')