from import_export import resources
from .models import *

class EmpresaResource(resources.ModelResource):
    class Meta:
        model = Empresa

class CliProResource(resources.ModelResource):
    class Meta:
        model = CliPro

# class DetalleResource(resources.ModelResource):
#     class Meta:
#         model = Detalle