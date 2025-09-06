from django.db import models
class Driver(models.Model):
	name = models.CharField(max_length=100)
	phone = models.CharField(max_length=20)
	vehicle_type = models.CharField(max_length=50)
	vehicle_number = models.CharField(max_length=20)
	rating = models.FloatField(default=4.5)
	photo_url = models.URLField(blank=True, null=True)

	def __str__(self):
		return f"{self.name} ({self.vehicle_type})"

from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	from decimal import Decimal
	balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

	def __str__(self):
		return f"{self.user.username} Wallet"

class WalletTransaction(models.Model):
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	amount = models.DecimalField(max_digits=10, decimal_places=2)
	transaction_type = models.CharField(max_length=10, choices=(('credit', 'Credit'), ('debit', 'Debit')))
	description = models.CharField(max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.wallet.user.username} {self.transaction_type} {self.amount}" 

class Booking(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	vehicle_type = models.CharField(max_length=20)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	pickup = models.CharField(max_length=100)
	destination = models.CharField(max_length=100)
	status = models.CharField(max_length=20, default='Pending')
	can_cancel = models.BooleanField(default=True)
	driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
	vehicle_number = models.CharField(max_length=20, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.user.username} - {self.vehicle_type} ({self.status})"
