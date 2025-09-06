
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from core.models import Booking

# Admin dashboard view (stub)
@login_required
def admin_dashboard_view(request):
	# Demo: Only show if user is admin
	from accounts.models import UserProfile
	profile = UserProfile.objects.filter(user=request.user, is_admin=True).first()
	if profile:
		return render(request, 'core/admin_dashboard.html')
	return HttpResponseRedirect(reverse('home'))

@login_required
def booking_history_view(request):
	bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
	return render(request, 'core/booking_history.html', {'bookings': bookings})
# Cancel booking view
from core.models import Booking
@login_required
def cancel_booking_view(request):
	if request.method == 'POST':
		booking_id = request.POST.get('booking_id')
		booking = Booking.objects.filter(id=booking_id, user=request.user, can_cancel=True, status='Confirmed').first()
		if booking:
			booking.status = 'Cancelled'
			booking.can_cancel = False
			booking.save()
	return HttpResponseRedirect(reverse('booking_history'))

# Submit feedback view (demo)
@login_required
def submit_feedback_view(request):
	if request.method == 'POST':
		# For demo, just redirect. You can store feedback in a model if needed.
		return HttpResponseRedirect(reverse('booking_history'))
	return HttpResponseRedirect(reverse('booking_history'))

@login_required
def add_wallet_balance_view(request):
	wallet = Wallet.objects.filter(user=request.user).first()
	if request.method == 'POST':
		amount = request.POST.get('amount')
		if amount and wallet:
			from decimal import Decimal
			wallet.balance += Decimal(amount)
			wallet.save()
	return render(request, 'core/add_wallet_balance.html', {'wallet': wallet})

from django.shortcuts import render

def contact_view(request):
	return render(request, 'core/contact.html')

def about_view(request):
	return render(request, 'core/about.html')



from core.models import Wallet
from django.contrib.auth.decorators import login_required

def home_view(request):
	vehicles = None
	pickup = destination = promocode = None
	discount = 0
	# Demo rental payment logic
	if request.method == 'POST' and 'rent_vehicle_type' in request.POST:
		# Demo: treat payment as always successful
		vehicle_type = request.POST.get('rent_vehicle_type')
		price = request.POST.get('rent_price')
		payment_method = request.POST.get('payment_method')
		Booking.objects.create(
			user=request.user,
			vehicle_type=vehicle_type,
			price=price,
			pickup='Rental',
			destination='Rental',
			status='Rented',
		)
		return render(request, 'core/booking_success.html', {
			'vehicle_type': vehicle_type,
			'price': price,
			'pickup': 'Rental',
			'destination': 'Rental',
			'payment_method': payment_method,
			'promocode': '',
			'discount': 0,
		})
	if request.method == 'POST' and 'vehicle_type' not in request.POST:
		pickup = request.POST.get('pickup')
		destination = request.POST.get('destination')
		promocode = request.POST.get('promocode', '').strip().lower()
		# Promocode logic
		promocodes = {
			'freefirst': 100,
			'save50': 50,
			'ride10': 10,
			'car20': 20,
		}
		if promocode in promocodes:
			discount = promocodes[promocode]
		if pickup and destination:
			# Calculate distance using Nominatim API (OpenStreetMap)
			import requests
			def get_coords(place):
				url = f'https://nominatim.openstreetmap.org/search?format=json&q={place}'
				try:
					resp = requests.get(url, timeout=5)
					data = resp.json()
					if data:
						return float(data[0]['lat']), float(data[0]['lon'])
				except Exception:
					pass
				return None, None

			lat1, lon1 = get_coords(pickup)
			lat2, lon2 = get_coords(destination)
			def haversine(lat1, lon1, lat2, lon2):
				from math import radians, sin, cos, sqrt, atan2
				R = 6371.0
				dlat = radians(lat2 - lat1)
				dlon = radians(lon2 - lon1)
				a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
				c = 2 * atan2(sqrt(a), sqrt(1-a))
				return R * c

			if lat1 is None or lat2 is None:
				dist = 10  # fallback default, show all vehicles
				filtered = [
					{'type': 'Bike', 'base': 30, 'per_km': 8},
					{'type': 'Mini', 'base': 50, 'per_km': 12},
					{'type': 'Sedan', 'base': 80, 'per_km': 15},
					{'type': 'SUV', 'base': 120, 'per_km': 20},
					{'type': 'Auto', 'base': 40, 'per_km': 10},
					{'type': 'Luxury', 'base': 250, 'per_km': 40},
					{'type': 'Electric', 'base': 60, 'per_km': 10},
				]
			else:
				dist = haversine(lat1, lon1, lat2, lon2)
				vehicle_types = [
					{'type': 'Bike', 'base': 30, 'per_km': 8},
					{'type': 'Mini', 'base': 50, 'per_km': 12},
					{'type': 'Sedan', 'base': 80, 'per_km': 15},
					{'type': 'SUV', 'base': 120, 'per_km': 20},
					{'type': 'Auto', 'base': 40, 'per_km': 10},
					{'type': 'Luxury', 'base': 250, 'per_km': 40},
					{'type': 'Electric', 'base': 60, 'per_km': 10},
				]
				filtered = []
				for v in vehicle_types:
					if dist < 15:
						filtered.append(v)
					elif 15 <= dist < 45:
						if v['type'] != 'Bike':
							filtered.append(v)
					elif 45 <= dist < 120:
						if v['type'] not in ['Bike', 'Mini']:
							filtered.append(v)
					elif 120 <= dist < 350:
						if v['type'] not in ['Bike', 'Mini', 'Sedan']:
							filtered.append(v)
					elif dist >= 350:
						# For very long routes, always show SUV and Luxury
						if v['type'] in ['SUV', 'Luxury']:
							filtered.append(v)
			vehicles = []
			for v in filtered:
				price = v['base'] + v['per_km'] * dist
				# Apply discount if promocode is valid
				if discount:
					price = price * (1 - discount/100)
				vehicles.append({'type': v['type'], 'price': int(price)})
	return render(request, 'core/home.html', {
		'vehicles': vehicles,
		'pickup': pickup,
		'destination': destination,
		'promocode': promocode,
		'discount': discount,
	})

@login_required
def book_vehicle_view(request):
	user = request.user
	wallet = Wallet.objects.filter(user=user).first()
	if request.method == 'POST':
		vehicle_type = request.POST.get('vehicle_type')
		price = request.POST.get('price')
		pickup = request.POST.get('pickup')
		destination = request.POST.get('destination')
		payment_method = request.POST.get('payment_method')
		promocode = request.POST.get('promocode', '').strip().lower()
		# Promocode logic
		promocodes = {
			'freefirst': 100,
			'save50': 50,
			'ride10': 10,
			'car20': 20,
		}
		discount = promocodes.get(promocode, 0)
		if discount:
			from decimal import Decimal
			price = Decimal(price) * (Decimal('1') - Decimal(discount)/Decimal('100'))
			price = str(int(price))
		# Payment logic here (wallet, card, UPI, etc.)
		from decimal import Decimal
		price_decimal = Decimal(price)
		if payment_method == 'wallet' and wallet:
			if wallet.balance >= price_decimal:
				wallet.balance -= price_decimal
				wallet.save()
		# Save booking to database
		Booking.objects.create(
			user=user,
			vehicle_type=vehicle_type,
			price=price_decimal,
			pickup=pickup,
			destination=destination,
			status='Confirmed',
		)
		return render(request, 'core/booking_success.html', {
			'vehicle_type': vehicle_type,
			'price': price,
			'pickup': pickup,
			'destination': destination,
			'payment_method': payment_method,
			'promocode': promocode,
			'discount': discount,
		})
	vehicle_type = request.GET.get('vehicle_type')
	price = request.GET.get('price')
	pickup = request.GET.get('pickup')
	destination = request.GET.get('destination')
	return render(request, 'core/booking.html', {
		'vehicle_type': vehicle_type,
		'price': price,
		'pickup': pickup,
		'destination': destination,
		'wallet': wallet,
	})
