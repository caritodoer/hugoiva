from import_export import resources
from .models import Empresa, CliPro


class EmpresaResource(resources.ModelResource):
    class Meta:
        model = Empresa


class CliProResource(resources.ModelResource):
    class Meta:
        model = CliPro
