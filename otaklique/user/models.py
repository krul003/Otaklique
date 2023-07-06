from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image

# Create your models here.
class MyUserManager(BaseUserManager):
	def _create_user(self, first_name, last_name, username, email, password, is_staff, is_superuser, is_admin, **extra_fields):
		now = timezone.now()
		if not first_name:
			raise ValueError('Users must have a first name.')
		if not last_name:
			raise ValueError('Users must have a last name.')
		if not username:
			raise ValueError('Users must have an username.')
		if not email:
			raise ValueError('Users must have an email address.')
		user = self.model(
				first_name = first_name,
				last_name = last_name,
				username = username,
				email =	self.normalize_email(email),
				is_staff = is_staff,
				is_superuser = is_superuser,
				is_admin = is_admin,
				last_login = now,
				date_joined = now,
				**extra_fields
			)
		user.set_password(password)
		user.save(using = self._db)
		return user

	def create_user(self, first_name, last_name, username, email, password=None, **extra_fields):
		user = self._create_user(first_name, last_name, username, email, password, False, False, False,**extra_fields)
		return user

	def create_superuser(self, first_name, last_name, username, email, password, **extra_fields):
		user = self._create_user(first_name, last_name, username, email, password, True, True, True,**extra_fields)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	first_name = models.CharField(max_length = 30, blank = False)
	last_name = models.CharField(max_length = 30, blank = False)
	username  = models.CharField(max_length = 30, unique = True, blank = False)
	email = models.EmailField(max_length = 50, unique = True, blank = False)
	date_joined = models.DateTimeField(auto_now_add = True)
	date_joined = models.DateTimeField(auto_now_add = True)
	is_admin = models.BooleanField(default = False)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_superuser = models.BooleanField(default = False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['first_name','last_name','email']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_full_name(self):
		return self.username

	def get_short_name(self):
		return self.username

class ProfilePicture(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	profile_image = models.ImageField(default = 'profile_default.png', upload_to = 'profile_pics')

	class Meta:
		verbose_name = 'profilepicture'
		verbose_name_plural = 'profilepictures'

	def __str__(self):
		return f'{self.user.username} Profile Picture'

class CoverPicture(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	cover_image = models.ImageField(default = 'cover_default.jpg', upload_to = 'cover_pics')

	class Meta:
		verbose_name = 'coverpicture'
		verbose_name_plural = 'coverpictures'

	def __str__(self):
		return f'{self.user.username} Cover Picture'
