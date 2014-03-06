from django import forms
from bookmarks.models import Link, List
from django.contrib.auth.models import User

class ListForm(forms.ModelForm):
	name = forms.CharField(max_length = 50, help_text="Enter the name of the list:")

	class Meta:
			model = List

class LinkForm(forms.ModelForm):
	name = forms.CharField(max_length = 50, help_text="Name")
	link = forms.URLField(max_length=200, help_text="URL")
	tags = forms.CharField(help_text = "Tags")

	class Meta:
		model = Link
		fields = ('name', 'link', 'tags')

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password' )

class DeleteForm(forms.ModelForm):
	class Meta:
		model = Link
		fields = []


