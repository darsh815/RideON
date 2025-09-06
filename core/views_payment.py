from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from core.models import Booking
import razorpay

# Razorpay keys (test mode)
RAZORPAY_KEY_ID = 'rzp_test_YourKeyHere'
RAZORPAY_KEY_SECRET = 'YourSecretHere'

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.status != 'Completed':
        return redirect('home')
    amount = int(booking.price * 100)  # Razorpay expects paise
    order = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
    context = {
        'booking': booking,
        'order_id': order['id'],
        'razorpay_key_id': RAZORPAY_KEY_ID,
        'amount': amount,
    }
    return render(request, 'core/payment.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        booking.status = 'Paid'
        booking.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})
