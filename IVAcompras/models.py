from django.db import models
from django.core.urlresolvers import reverse 
from django.core.validators import MinValueValidator
from decimal import Decimal

class Empresa(models.Model):
	nombre = models.CharField(max_length=50, unique=True)
	propietario = models.CharField(max_length=50)
	cuit = models.CharField("CUIT", max_length=13, unique=True)
	localidad = models.CharField(max_length=50)
	direccion = models.CharField(max_length=50)
	telefono = models.CharField(max_length=50, null=True, blank=True)
	directorio = models.CharField(max_length=50)

	def get_absolute_url(self):
		return reverse("iva:v_empresa", kwargs={"id":self.id})

	def go_home(self):
		return reverse("iva:home")

	def __str__(self):
		return ('%s - %s')%(self.nombre, self.cuit)

class CliPro(models.Model):
	nombre = models.CharField("Razón Social", max_length=30, unique=True)
	direccion = models.CharField(max_length=30)
	telefono = models.CharField(max_length=30, null=True, blank=True)
	cuit = models.CharField("C.U.I.T.", max_length=13, unique=True)
	es_cliente = models.BooleanField(default=False)
	es_proveedor = models.BooleanField(default=False)
	iva_choices = (
		('CF', 'Consumidor Final'),
		('I', 'Inscripto'),
		('NI', 'No Inscripto'),
		('M', 'Monotributo'),
		('E', 'Exento'),
		)
	iva = models.CharField("Tipo I.V.A.", max_length=30, choices=iva_choices)
	obs = models.TextField("Observaciones", null=True, blank=True)

	def get_absolute_url(self):
		return reverse("iva:v_cli_pro", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s - %s')%(self.nombre, self.cuit, self.iva)

class Libro(models.Model):
	empresa = models.ForeignKey(Empresa)
	tipo_libro_choices = (
		('V', 'Libro Ventas'),
		('C', 'Libro Compras'),
		) 
	tipo_libro = models.CharField("Tipo de Libro", max_length=1, choices=tipo_libro_choices)

	def get_absolute_url(self):
		return reverse("iva:v_libro", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s')%(self.empresa, self.tipo_libro)

	class Meta:
		unique_together = ("empresa", "tipo_libro")

class Detalle(models.Model):
	libro = models.ForeignKey(Libro)
	fecha = models.DateField(auto_now=False, null=True)
	tipo_comprobante_choices = (
		('F', 'Factura'),
		('ND', 'Nota de Débito'),
		('NC', 'Nota de Crédito'),
		('R', 'Recibo'),
		)
	tipo_comprobante = models.CharField("Comprobante", max_length=2, choices= tipo_comprobante_choices, null=True)
	letra = models.CharField("Letra", max_length=1, null=True)
	sucursal = models.CharField("Sucursal", max_length=3, null=True)
	nfactura = models.CharField("N°", max_length=30, null=True)
	cli_pro = models.ForeignKey(CliPro, verbose_name="Cliente/Proveedor", null=True)
	
	gravado = models.DecimalField("Gravado", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	no_gravado = models.DecimalField("No Gravado", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	iva21 = models.DecimalField("I.V.A. 21%", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	iva105= models.DecimalField("I.V.A. 10,5%", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	iva_otros= models.DecimalField("Otros I.V.A.", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	rg2126= models.DecimalField("R.G. 2126", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	ret_IVA = models.DecimalField("Ret. I.V.A.", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	ret_iibb= models.DecimalField("Ret. IIBB", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	imp_int= models.DecimalField("Imp. Internos", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
	otros= models.DecimalField("Otros", default=0, null=True, decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])

	
	def get_absolute_url(self):
		return reverse("iva:v_detalle", kwargs={"id":self.id})

	def __str__(self):
		return ('%s - %s - %s - %s')%(self.libro, self.fecha, self.nfactura, self.cli_pro)

	class Meta:
		unique_together = ("libro", "tipo_comprobante", "nfactura", "letra")

