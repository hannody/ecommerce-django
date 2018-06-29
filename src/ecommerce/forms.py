from django import forms

class ContactForm(forms.Form):

	fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Your fullname"}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"Your email"}))
	content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "placeholder":"Your content"}))


	# for validation, just use def followed by clean_TheNameOfTheFieldToValidate
	def clean_email(self):
		email = self.cleaned_data.get("email")
		if not  "gmail.com" in email:
			raise forms.ValidationError("please enter a valid email that ends with .com or.net etc..")
		return email