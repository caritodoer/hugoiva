from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from crispy_forms.helper import FormHelper
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, Field, ButtonHolder
from crispy_forms.bootstrap import StrictButton, FieldWithButtons, PrependedText, PrependedAppendedText, FormActions

User = get_user_model()

class UserLoginForm(forms.Form):
	username = forms.CharField(label='Usuario')
	password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')

	def clean(self, *args, **kwargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username, password=password)
			if not user:
				raise forms.ValidationError("El nombre de Usuario no es correcto.")

			if not user.check_password(password):
				raise forms.ValidationError("La contraseña no es correcta.")

			if not user.is_active:
				raise forms.ValidationError("Este Usuario ya no esta activo.")
		return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
	username = forms.CharField(label='Usuario', help_text='150 caracteres o menos. Letras, digitos y @/./+/-/_ solamente.')
	password = forms.CharField(widget=forms.PasswordInput, label='Contraseña')
	email = forms.EmailField(label='Email')
	email2 = forms.EmailField(label='Confirme Email')
	class Meta:
		model = User
		fields = [
			'username',
			'password',
			'email',
			'email2',
		]
	def clean_email2(self):
		email = self.cleaned_data.get('email')
		email2 = self.cleaned_data.get('email2')
		if email != email2:
			raise forms.ValidationError("El e-mail no coincide")
		email_qs = User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("Este email ya fue registrado")

		return email

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)
		self.helper.form_id = 'id-UserRegisterForm'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'POST'
		self.helper.form_action = ''

		self.helper.label_class = 'col-lg-3 col-sm-3'
		self.helper.field_class = 'col-lg-8 col-sm-8'

		self.helper.add_input(Submit('submit', 'Enviar', css_class='btn-primary'))
	
