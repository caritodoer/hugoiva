from django.contrib import admin
from IVAcompras.models import Empresa, CliPro, Libro, Detalle
# Register your models here.
from import_export.admin import ImportExportModelAdmin

@admin.register(Empresa)
class EmpresaAdmin(ImportExportModelAdmin):
    pass
#admin.site.register(Empresa)

@admin.register(CliPro)
class CliProAdmin(ImportExportModelAdmin):
    pass
#admin.site.register(CliPro)
admin.site.register(Libro)

@admin.register(Detalle)
class DetalleAdmin(ImportExportModelAdmin):
    pass
#admin.site.register(Detalle)
