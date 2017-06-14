from django import forms
from .models import *

class ProveedorForm(forms.ModelForm):
	class Meta:
		model = Proveedor
		fields = [
			"razon_social",
			"cuit",
			"nombre_fantasia",
			"iva",
		]

class ClienteForm(forms.ModelForm):
	class Meta:
		model = Cliente
		fields = [
			"razon_social",
			"comercio",
			"domicilio",
			"cuit",
		]

class LibroForm(forms.ModelForm):
	class Meta:
		model = Libro
		fields = [
			"cliente",
			"mes",
			"anio",
			"fecha",
			"nfactura",
			"tipo",
			"proveedor",
			"ing_porcentaje",
			"ing",
			"cng",
			"op_ex",
			"iva_liq",
			"iva_rec",
			"total_fac",
			"cred_fisc",
			"ret_perc",
		] 