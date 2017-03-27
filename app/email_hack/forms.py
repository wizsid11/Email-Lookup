from django import forms
from .models import Emailfinder

class Form(forms.Form):
	file=forms.FileField(label='Select a file')
class Form1(forms.Form):
	name = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}))
	domain = forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Domain'}))
	# class Meta:
		# model = Emailfinder
		# fields= ['name','domain']
class LoginForm(forms.Form):
	username=forms.CharField(label='',widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email'}))
	password=forms.CharField(label='',widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))