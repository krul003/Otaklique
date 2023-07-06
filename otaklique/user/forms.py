from django import forms
from .models import User, ProfilePicture, CoverPicture
from django.contrib.auth.forms import UserCreationForm
from PIL import Image

class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(max_length = 30, label = False,widget = forms.TextInput(attrs = {'class':'form-control', 'type':'text','id':'inputtxt', 'name':'first_name', 'placeholder':'First Name', 'autocomplete':'off'}))
	last_name = forms.CharField(max_length = 30, label = False, widget = forms.TextInput(attrs = {'class':'form-control', 'type':'text','id':'inputtxt', 'name':'last_name', 'placeholder':'Last Name', 'autocomplete':'off'}))
	username  = forms.CharField(max_length = 30, label = False, widget = forms.TextInput(attrs = {'class':'form-control', 'type':'text','id':'inputtxt', 'name':'username', 'placeholder':'Username', 'autocomplete':'off'}),)
	email = forms.EmailField(max_length = 50, label = False, widget = forms.EmailInput(attrs = {'class':'form-control', 'type':'email','id':'inputtxt', 'name':'email', 'placeholder':'Email-Address', 'autocomplete':'off'}))
	password1 = forms.CharField(label = False, widget = forms.PasswordInput(attrs = {'class':'form-control', 'type':'password','id':'inputtxt','name':'password1', 'placeholder':'Password', 'autocomplete':'off'}))
	password2 = forms.CharField(label = False, widget = forms.PasswordInput(attrs = {'class':'form-control', 'type':'password','id':'inputtxt','name':'password2', 'placeholder':'Re-Enter Password', 'autocomplete':'off'}))
	class Meta: 
		model = User 
		fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
		field_order = ['first_name','last_name','username', 'email', 'password1', 'password2']

	def clean(self):
		cleaned_data = super(UserRegisterForm, self).clean()
		if 'password1' in self.cleaned_data	and 'password2' in self.cleaned_data:
			if self.cleaned_data['password1'] != self.cleaned_data['password2']:
				raise forms.ValidationError("Password don't match.")
		return self.cleaned_data

	def save(self, commit = True):
		user = super(UserRegisterForm, self).save(commit = False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user

class AuthenticationForm(forms.Form):
	username = forms.CharField(label = False, widget = forms.TextInput(attrs = {'class':'form-control', 'type':'text','id':'inputtxt', 'name':'username', 'placeholder':'Username', 'autocomplete':'off'}))
	password = forms.CharField(label = False, widget = forms.PasswordInput(attrs = {'class':'form-control', 'type':'password','id':'inputtxt','name':'password', 'placeholder':'Password', 'autocomplete':'off'}))
	class Meta:
		fields = ['username', 'password']

class ProfileUpdateForm(forms.ModelForm):
	profile_image = forms.ImageField(label = False)
	x = forms.FloatField(widget = forms.HiddenInput())
	y = forms.FloatField(widget = forms.HiddenInput())
	width = forms.FloatField(widget = forms.HiddenInput())
	height = forms.FloatField(widget = forms.HiddenInput())
	
	class Meta:
		model = ProfilePicture
		fields = ['profile_image','x','y','width','height']

	def save(self):
		photo = super(ProfileUpdateForm, self).save()

		x = self.cleaned_data.get('x')
		y = self.cleaned_data.get('y')
		w = self.cleaned_data.get('width')
		h = self.cleaned_data.get('height')

		image = Image.open(photo.profile_image)
		cropped_image = image.crop((x,y,w+x,h+y))
		resized_image = cropped_image.resize((200,200), Image.ANTIALIAS)
		resized_image.save(photo.profile_image.path)

		return photo

class CoverUpdateForm(forms.ModelForm):
	cover_image = forms.ImageField(label = False)
	x = forms.FloatField(widget = forms.HiddenInput())
	y = forms.FloatField(widget = forms.HiddenInput())
	width = forms.FloatField(widget = forms.HiddenInput())
	height = forms.FloatField(widget = forms.HiddenInput())

	class Meta:
		model = CoverPicture
		fields = ['cover_image', 'x', 'y', 'width', 'height']

	def save(self):
		photo = super(CoverUpdateForm, self).save()

		x = self.cleaned_data.get('x')
		y = self.cleaned_data.get('y')
		w = self.cleaned_data.get('width')
		h = self.cleaned_data.get('height')

		image = Image.open(photo.cover_image)
		cropped_image = image.crop((x,y,w+x,h+y))
		resized_image = cropped_image.resize((1100,400), Image.ANTIALIAS)
		resized_image.save(photo.cover_image.path)

		return photo