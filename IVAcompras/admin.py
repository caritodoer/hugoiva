from django.contrib import admin

# Register your models here.
from IVAcompras.models import Empresa, CliPro, Libro, Detalle
# Register your models here.

admin.site.register(Empresa)
admin.site.register(CliPro)
admin.site.register(Libro)
admin.site.register(Detalle)
