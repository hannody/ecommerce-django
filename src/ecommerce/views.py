from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model




def home_page(request):
	content= {
		"title":"Welcome to this ECommerece Portal!",
		"content": "Free Content.",
	}

	if request.user.is_authenticated():
		content ["premium_content"]= "Yahhh!"
	return render(request, 'home_page.html', content)

def about_page(request):
	content= {
		"title":"About",
		"content": "Welcome to the About Page."
	}
	return render(request, 'about_page.html', content)


def login_page(request):

	form = LoginForm(request.POST or None)

	context = {"form":form}

	if form.is_valid():

		print(form.cleaned_data)

		username = form.cleaned_data.get('username')

		password = form.cleaned_data.get('password')

		user = authenticate(request, username=username, password=password)


		print(request.user.is_authenticated())
		if user is not None:
			print(request.user.is_authenticated())
			login(request, user)

			return redirect("/login")
			# Redirect to a success page.
		else:
			print("Error in Logining In!")

	return render(request, 'auth/login.html', context)


User = get_user_model()

def register_page(request):
	form = RegisterForm(request.POST or None)
	context = {"form":form}
	if form.is_valid():

		#print("form.cleaned_data= ", form.cleaned_data)

		username = form.cleaned_data.get('username')

		email = form.cleaned_data.get('email')

		password = form.cleaned_data.get('password')

		new_user = User.objects.create_user(username, email, password)

		#print(new_user)

	return render(request, 'auth/register.html',context)


def contact_page(request):

	contact_form = ContactForm(request.POST or None)


	content= {
		"title":"Contact Us",
		"content": "Welcome to the Contact Page.",
		"form": contact_form,
	}

	if contact_form.is_valid():
		print(contact_form.cleaned_data)

	#print(request.POST)
	#print(request.POST.get('fullname'))
	return render(request, 'contact/view.html', content)
