from django.shortcuts import render
from django.http import HttpResponse
from .forms import ContactForm

def home_page(request):
	content= {
		"title":"Home",
		"content": "Welcome to the Home Page."
	}
	return render(request, 'home_page.html', content)

def about_page(request):
	content= {
		"title":"About",
		"content": "Welcome to the About Page."
	}
	return render(request, 'home_page.html', content)

def contact_page(request):

	contact_form = ContactForm(request.POST or None)


	content= {
		"title":"Contact",
		"content": "Welcome to the Contact Page.",
		"form": contact_form,
	}

	if contact_form.is_valid():
		print(contact_form.cleaned_data)

	#print(request.POST)
	#print(request.POST.get('fullname'))
	return render(request, 'contact/view.html', content)