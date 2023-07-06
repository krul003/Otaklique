from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User, ProfilePicture, CoverPicture
# Register your models here.

class UserAdmin(BaseUserAdmin):
	list_display = ('username','email','last_login','is_active','is_staff')
	list_filter = ('is_staff','is_active')
	fieldsets = ((None, {'fields':('first_name','last_name','username','email','password')}), ('Permissions',{'fields':('is_staff','is_active','is_superuser','is_admin')}),)
	add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')}),)
	search_fields =('username',)
	ordering = ('username',)
	filter_horizontal = ()
	
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(ProfilePicture)
admin.site.register(CoverPicture)