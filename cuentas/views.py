from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm
from django.views.decorators.http import require_auth
# Create your views here.

def login_view(request):
	title = 'Bienvenido'
	form = UserLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username=username, password=password)
		login(request, user)
		if request.user.is_authenticated:
			return redirect("/home")
	context = {
		"title": title,
		"form": form, 
	}
	return render(request, "login_form.html", context)

@require_auth
def register_view(request):
	title = "Registrar Usuario"
	form = UserRegisterForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		password = form.cleaned_data.get('password')
		user.set_password(password)
		user.save()

		return redirect("/usuarios")

	context = {
		"title": title,
		"form": form, 
	}
	return render(request, "altas.html", context)

def logout_view(request):
	logout(request)
	return render(request, "logout_form.html", {})