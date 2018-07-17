from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

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



class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Username"}))
	
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"Choose a password"}))


class RegisterForm(forms.Form):
	
	username = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Type in your username"}))
	
	email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"Type in your email"}))
	
	password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"Choose a password"}))
	
	password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"re-enter your password"}))

# to prevent registring a previuosly exited/used/taken usename
	def clean_username(self):
		username = self.cleaned_data.get("username")

		if len(username) < 6:
			raise forms.ValidationError("Username should be longer than six charachters!")
		else:

			qs = User.objects.filter(username = username)

			if qs.exists():
				raise forms.ValidationError("Username is taken!")
			return username

# to prevent registring a previuosly exited/used email address!
	def clean_email(self):
		email = self.cleaned_data.get("email")

		qs = User.objects.filter(email = email)

		if qs.exists():
			raise forms.ValidationError("this email is already registered!")
		return email
# Password Validation
	def clean(self):
		
		data = self.cleaned_data

		password = self.cleaned_data.get("password")
		
		password2 = self.cleaned_data.get("password2")
		
		if password2 != password:
			raise forms.ValidationError("Passwords must match!")


		if validate_password(password):
			return data


# Password validation(src= https://docs.djangoproject.com/en/2.0/_modules/django/contrib/auth/password_validation/)
import functools
import gzip
import os
import re
from difflib import SequenceMatcher

from django.conf import settings
from django.core.exceptions import (
    FieldDoesNotExist, ImproperlyConfigured, ValidationError,
)
from django.utils.functional import lazy
from django.utils.html import format_html
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _, ngettext


@functools.lru_cache(maxsize=None)
def get_default_password_validators():
	return get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)

def validate_password(password, user=None, password_validators=None):
    """
    Validate whether the password meets all validator requirements.

    If the password is valid, return ``None``.
    If the password is invalid, raise ValidationError with all error messages.
    """
    errors = []
    if password_validators is None:
        password_validators = get_default_password_validators()
    for validator in password_validators:
        try:
            validator.validate(password, user)
        except ValidationError as error:
            errors.append(error)
    if errors:
        raise ValidationError(errors)

    return True


def get_password_validators(validator_config):
    validators = []
    for validator in validator_config:
        try:
            klass = import_string(validator['NAME'])
        except ImportError:
            msg = "The module in NAME could not be imported: %s. Check your AUTH_PASSWORD_VALIDATORS setting."
            raise ImproperlyConfigured(msg % validator['NAME'])
        validators.append(klass(**validator.get('OPTIONS', {})))
    return validators
#