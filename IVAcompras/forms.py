from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout
from crispy_forms.bootstrap import StrictButton
from .models import *

class CliProForm(forms.ModelForm):
	class Meta:
		model = CliPro
		fields = [
			"nombre",
			"direccion",
			"telefono",
			"cuit",
			"es_cliente",
			"es_proveedor",
			"iva",
			"obs",
		]
	def __init__(self, *args, **kwargs):
		super(CliProForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)
		self.helper.form_id = 'id-CliProForm'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'POST'
		self.helper.form_action = ''

		self.helper.label_class = 'col-lg-3 col-sm-3'
		self.helper.field_class = 'col-lg-8 col-sm-8'

		self.helper.add_input(Submit('submit', 'Enviar', css_class='btn-primary'))
	

class EmpresaForm(forms.ModelForm):
	class Meta:
		model = Empresa
		fields = [
			"nombre",
			"propietario",
			"cuit",
			"localidad",
			"direccion",
			"telefono",
			"directorio",
		]
	def __init__(self, *args, **kwargs):
		super(EmpresaForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)
		self.helper.form_id = 'id-EmpresaForm'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'POST'
		self.helper.form_action = ''
	
		self.helper.label_class = 'col-lg-3 col-sm-3'
		self.helper.field_class = 'col-lg-8 col-sm-8'

		self.helper.add_input(Submit('submit', 'Enviar', css_class='btn-primary'))
		#self.helper.layout.append(Submit('save', 'save'))



class LibroForm(forms.ModelForm):
	class Meta:
		model = Libro
		fields = [
			"empresa",
			"tipo_libro",
		] 
	def __init__(self, *args, **kwargs):
		super(LibroForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)
		self.helper.form_id = 'id-LibroForm'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'POST'
		self.helper.form_action = ''

		self.helper.label_class = 'col-lg-3 col-sm-3'
		self.helper.field_class = 'col-lg-8 col-sm-8'

		self.helper.add_input(Submit('submit', 'Enviar', css_class='btn-primary'))
		#self.helper.layout.append(Submit('save', 'save'))

class DetalleForm(forms.ModelForm):
	class Meta:
		model = Detalle
		fields = [
			"libro",
			"fecha",
			"tipo_comprobante",
			"nfactura",
			"cli_pro",
			"alic",
			"importe",
			"ex_iva_insc",
			"ex_19640",
			"ret",
		]
		
	def __init__(self, *args, **kwargs):
		super(DetalleForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)
		self.helper.form_id = 'id-DetalleForm'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'POST'
		self.helper.form_action = ''

		self.helper.label_class = 'col-lg-3 col-sm-3'
		self.helper.field_class = 'col-lg-8 col-sm-8'

		self.helper.add_input(Submit('submit', 'Enviar', css_class='btn-primary'))
		

