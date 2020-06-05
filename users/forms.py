from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from .models import Profile




class NewSetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						'class':'form-control',
						'type' : 'password'
					}
				),
			label = 'New Password'
		)

	new_password2 = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						'class':'form-control',
						'type' : 'password'
					}
				),
			label = 'New Password Confirmation'
		)		



class NewPasswordResetConfirmView(PasswordResetConfirmView):
	form_class = NewSetPasswordForm


class NewPasswordResetForm(PasswordResetForm):
	email = forms.EmailField(
    		widget=forms.EmailInput(
    				attrs = {
    					'class' : 'form-control',
    					'type' : 'email'
    				}
    			), max_length=200, help_text='Required'
    	)



class NewPasswordResetView(PasswordResetView):
	form_class = NewPasswordResetForm



class MyAuthForm(AuthenticationForm):
	username =forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form-control',
						
					}
				),
			label = 'Username'
		)

	password = forms.CharField(
    		widget=forms.PasswordInput(
    				attrs={
    					'class':'form-control',
    					'type':'password'
    				}
    			)	
    	)

	error_messages = {
        'invalid_login': _(
            "Username atau Password anda salah. Mohon periksa kembali."
            # "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }




class MyLoginView(LoginView):
    authentication_form = MyAuthForm


class UserRegisterForm(UserCreationForm):
	first_name = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form-control'
					}
				)
		)
	
	last_name = forms.CharField(
			widget=forms.TextInput(
					attrs={
						'class':'form-control'
					}
				)
		)

	username = forms.CharField(
			widget=forms.TextInput(
					attrs={
						'class':'form-control'
					}
				)
		)

	email = forms.EmailField(
    		widget=forms.EmailInput(
    				attrs = {
    					'class' : 'form-control',
    					'type' : 'email'
    				}
    			), max_length=200, help_text='Required'
    	)

	password1 = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						'class':'form-control',
						'type' : 'password'
					}
				),
			label = 'Password'
		)

	password2 = forms.CharField(
			widget=forms.PasswordInput(
					attrs = {
						'class':'form-control',
						'type' : 'password'
					}
				),
			label = 'Password Confirmation'
		)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'username', 'email']


class ProfileForm(forms.ModelForm):
	FAKULTAS = (
			('BIO', 'biologi'),
			('FAPERTA', 'pertanian'),
			('FTP', 'ftp'),
		)

	JURUSAN = (
			('MATEMATIKA', 'matematika'),
			('Fisika', 'fisika'),
			('SISTEM INFORMASI', 'si'),
		)

	NIM = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form-control'
					}
				)
		)

	fakultas = forms.ChoiceField(choices=FAKULTAS,
			widget=forms.Select(
					attrs = {
						'class':'form-control'
					}
				)
		)
	jurusan = forms.ChoiceField(choices=JURUSAN,
			widget=forms.Select(
					attrs = {
						'class':'form-control'
					}
				)
		)
	nohp = forms.CharField(
			widget=forms.TextInput(
					attrs = {
						'class':'form-control',
						'type':'number',
					}
				), label='Nomor Handphone (Whatsapp)'
		)
	class Meta:
         model = Profile
         fields = (
         	'NIM', 
         	'fakultas',
         	'jurusan',
         	'nohp',
         	)