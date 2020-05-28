from django.db import models
from django.contrib.auth.models import User
# from PIL import Image

class Profile(models.Model):
	user 	= models.OneToOneField(User, on_delete = models.CASCADE)
	image 	= models.ImageField(default='default_profile.jpg', upload_to='profile_pics', blank=True, null=True)
	NIP		= models.CharField(max_length=255, blank=True)
	NIK		= models.CharField(max_length=255, blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'
		

	def save(self, *args, **kwargs):
		super(Profile, self).save(*args, **kwargs)