from core import views_payment
    path('pay/<int:booking_id>/', views_payment.payment_page, name='payment_page'),
    path('payment_success/', views_payment.payment_success, name='payment_success'),
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('book/', views.book_vehicle_view, name='book_vehicle'),
    path('booking_history/', views.booking_history_view, name='booking_history'),
    path('add_wallet_balance/', views.add_wallet_balance_view, name='add_wallet_balance'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('cancel_booking/', views.cancel_booking_view, name='cancel_booking'),
    path('submit_feedback/', views.submit_feedback_view, name='submit_feedback'),
    path('pay/<int:booking_id>/', views_payment.payment_page, name='payment_page'),
    path('payment_success/', views_payment.payment_success, name='payment_success'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('book/', views.book_vehicle_view, name='book_vehicle'),
    path('booking_history/', views.booking_history_view, name='booking_history'),
    path('add_wallet_balance/', views.add_wallet_balance_view, name='add_wallet_balance'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
]

urlpatterns += [
    path('cancel_booking/', views.cancel_booking_view, name='cancel_booking'),
    path('submit_feedback/', views.submit_feedback_view, name='submit_feedback'),
]
