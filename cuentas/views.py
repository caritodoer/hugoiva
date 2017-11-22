from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, login, logout
from .forms import UserLoginForm, UserRegisterForm
# Create your views here.

def login_view(request):
	title = 'Bienvenido'
	#print(request.user.is_authenticated())
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		#print(request.user.is_authenticated())
		if request.user.is_authenticated:
			return redirect("/home")
	context = {
		"title": title,
		"form": form, 
	}
	return render(request, "login_form.html", context)

def register_view(request):
	print(request.user.is_authenticated())
	title = "Registrar"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()

		#new_user = authenticate(username=user.username, password=password)
		#login(request, user)
		return redirect("/usuarios")

	context = {
		"title": title,
		"form": form, 
	}
	return render(request, "altas.html", context)

def logout_view(request):
	logout(request)
	return render(request, "logout_form.html", {})