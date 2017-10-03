from django import forms
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
			"directorio"
		]

class LibroForm(forms.ModelForm):
	class Meta:
		model = Libro
		fields = [
			"empresa",
			"tipo_libro",
		] 

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
