from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate as django_authenticate
from django.contrib.auth.decorators import login_required 
from .forms import UserRegisterForm, AuthenticationForm, ProfileUpdateForm, CoverUpdateForm
from django.core.mail import send_mail 
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template 
from django.template import Context 
from .models import ProfilePicture, CoverPicture


def index(request): 
	return render(request, 'user/index.html', {'title':'index'})

def login(request):
	if request.method == 'POST':
		form = AuthenticationForm(data = request.POST)
		if form.is_valid:
			username = request.POST['username']
			password = request.POST['password']
			user = django_authenticate(username = username, password = password)
			if user is not None:
				if user.is_active:
					django_login(request, user)
					messages.success(request, f' welcome {username} ')
					return redirect('index')
			else:
				messages.info(request, f' Username or password invalid.')	
	else:
		form = AuthenticationForm()
	return render(request, 'user/login.html',{'form':form, 'title':'Log In'})

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(data = request.POST)
		if form.is_valid(): 
			form.save()
			username = request.POST['username']
			email = request.POST['email']
			htmly = get_template('user/Email.html') 
			d = { 'username': username } 
			subject, from_email, to = 'welcome', 'otaklique@gmail.com', email 
			html_content = htmly.render(d) 
			msg = EmailMultiAlternatives(subject, html_content, from_email, [to]) 
			msg.attach_alternative(html_content, "text/html") 
			msg.send()
			messages.success(request, f'Your account has been successfully created')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'user/register.html',{'form':form, 'title':'Sign Up'})

@login_required
def profile(request):
	p_photos = ProfilePicture.objects.all()
	c_photos = CoverPicture.objects.all()
	if request.method == 'POST':
		p_form = ProfileUpdateForm(request.POST,
									request.FILES,
									instance=request.user.profilepicture)
		c_form = CoverUpdateForm(request.POST,
								 request.FILES,
								 instance=request.user.coverpicture)
		if p_form.is_valid():
			p_form.save()
			messages.success(request, f'Your account has been successfully updated!')
			return redirect('profile')
		elif c_form.is_valid():
			c_form.save()
			messages.success(request, f'Your account has been successfully updated!')
			return redirect('profile')
	else:
		p_form = ProfileUpdateForm(instance=request.user.profilepicture)
		c_form = CoverUpdateForm(instance=request.user.coverpicture)
	
	context={
		'p_form' : p_form,
		'c_form' : c_form,
		'p_photos': p_photos,
		'c_photos': c_photos,
	}
	return render(request, 'user/profile.html',context)



