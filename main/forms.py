from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import ForumUser


class SignUpForm(UserCreationForm):
	first_name = forms.CharField()
	last_name = forms.CharField()
	username = forms.CharField()

	class Meta:
		model = ForumUser
		fields = ('first_name', 'last_name', 'username', 'email')


class ForumUserChangeForm(UserChangeForm):
	class Meta:
		model = ForumUser
		fields = ['first_name', 'last_name', 'username', 'email']


class ForumUserPasswordChangeForm(PasswordChangeForm):
	old_password = forms.PasswordInput()

	error_messages = {
		**PasswordChangeForm.error_messages,
		"password_incorrect": _(
			"Your old password was entered incorrectly. Please enter it again."
		),
		"passwords_unmatched": _(
			"New password do not match."
		)
	}

	class Meta:
		model = ForumUser
		fields = ('old_password', 'new_password1', 'new_password2')

	def check_old_password(self, request):
		user = request.user
		old_password = self.user['old_password']
		if not user.check_password(self.user['old_password']):
			raise ValidationError(
				self.error_messages['password_incorrect'],
				code="password_incorrect"
			)
		else:
			return True

	def check_new_passwords(self):
		if not self.user['new_password1'] == self.user['new_password2']:
			raise ValidationError(
				self.error_messages['passwords_unmatched'],
				code="passwords_unmatched"
			)
		else:
			return True

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.PasswordInput()

