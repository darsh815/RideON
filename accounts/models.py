
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	# Add more fields as needed (e.g., phone, is_driver)
	phone = models.CharField(max_length=15, blank=True)
	is_driver = models.BooleanField(default=False)

	def __str__(self):
		return self.user.username
