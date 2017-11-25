from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Fieldset, Div, Field, ButtonHolder
from crispy_forms.bootstrap import StrictButton, FieldWithButtons, PrependedText, PrependedAppendedText, FormActions
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

		self.helper.add_input(Submit('submit', 'Enviar', css_id="nuevo_cliente", css_class='btn-primary'))
	
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
			"letra",
			"sucursal",
			"nfactura",
			"cli_pro",
			"gravado",
			"no_gravado",
			"iva21",
			"iva105",
			"iva_otros",
			"rg2126",
			"ret_IVA",
			"ret_iibb",
			"imp_int",
			"otros",
		]
		
	def __init__(self, *args, **kwargs):
		super(DetalleForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)
		self.helper.form_id = 'id-DetalleForm'
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'POST'
		self.helper.form_action = ''

		self.helper.label_class = 'col-lg-5 col-sm-5'
		self.helper.field_class = 'col-lg-7 col-sm-7'

		self.helper.layout = Layout(
			Field('libro', value="{{libro}}", type = "hidden"),
			Div(
				'fecha',
				"sucursal",
				'tipo_comprobante',
				css_class='col-sm-6',
			),
			Div(
				FieldWithButtons('cli_pro', StrictButton("Agregar", css_id="esteboton", data_toggle="modal", data_target="#acpmodal")),
				"letra",
				"nfactura",
				css_class='col-sm-6',
			),
			Div(
				Fieldset(
					'Valores',
					Div(
						PrependedText('gravado', '$'),
						PrependedText('no_gravado', '$'),
						PrependedText('iva21', '$'),
						PrependedText('iva105', '$'),
						PrependedText('iva_otros', '$'),
						css_class='col-sm-6',
					),
					Div(
						PrependedText('rg2126', '$'),
						PrependedText('ret_IVA', '$'),
						PrependedText('ret_iibb', '$'),
						PrependedText('imp_int', '$'),
						PrependedText('otros', '$'),
						css_class='col-sm-6',
					),
				),
				css_class='col-sm-12',
			),
			ButtonHolder(
				Submit('submit', 'Enviar', css_class='btn-primary pull-right')
			)
			# PrependedAppendedText('gravado', '$','.00')
		)

		# self.helper[3:5].wrap_together(Div, css_class='grupo1')
		# self.helper['tipo_comprobante'].wrap(Field, wrapper_class='tipocomprobante')
		# self.helper['letra'].wrap(Field, wrapper_class='letra')
		
		# self.helper[7:16].wrap_together(Fieldset, 'Otros Valores')

		#self.helper.add_input(Submit('submit', 'Enviar', css_class='btn-primary'))
		

