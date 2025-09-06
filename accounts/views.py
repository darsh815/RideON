from .models import UserProfile
from django.contrib.auth.decorators import login_required
@login_required
def edit_profile_view(request):
	profile = UserProfile.objects.get(user=request.user)
	if request.method == 'POST':
		phone = request.POST.get('phone')
		if phone:
			profile.phone = phone
			profile.save()
	return render(request, 'accounts/edit_profile.html', {'profile': profile})

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile

def register_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		phone = request.POST.get('phone', '')
		is_driver = request.POST.get('is_driver', False)
		user = User.objects.create_user(username=username, password=password)
		UserProfile.objects.create(user=user, phone=phone, is_driver=is_driver)
		return redirect('login')
	return render(request, 'accounts/register.html')

def login_view(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user:
			login(request, user)
			return redirect('home')
		else:
			return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
	return render(request, 'accounts/login.html')

def logout_view(request):
	logout(request)
	return redirect('login')
