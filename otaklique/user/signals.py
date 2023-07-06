from django.db.models.signals import post_save
from .models import User, ProfilePicture, CoverPicture
from django.dispatch import receiver

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		ProfilePicture.objects.create(user = instance)
		CoverPicture.objects.create(user = instance)

@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
	instance.profilepicture.save()
	instance.coverpicture.save()
