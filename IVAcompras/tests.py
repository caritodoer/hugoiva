from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Empresa, Libro

# Create your tests here.

class EmpresaTests(TestCase):
    def setUp(self):
        # Se ejecuta antes de CADA test, sobre una base vacía.
        self.empresa = Empresa.objects.create(
            nombre="Empresa de prueba",
            propietario="Alguien",
            cuit="20-11111111-1",
            localidad="Cordoba",
            direccion="Calle 1",
            directorio="prueba",
        )
    
    def test_get_absolute_url_apunta_al_detalle_de_la_empresa(self):
        self.assertEqual(self.empresa.get_absolute_url(), f"/v_empresa/{self.empresa.id}/")


class LibroTests(TestCase):

    def setUp(self):
        # Se ejecuta antes de CADA test, sobre una base vacía.
        self.empresa = Empresa.objects.create(
            nombre="Empresa de prueba",
            propietario="Alguien",
            cuit="20-11111111-1",
            localidad="Cordoba",
            direccion="Calle 1",
            directorio="prueba",
        )
    

    def test_no_permite_dos_libros_de_ventas_en_la_misma_empresa(self):
        # Arrange: ya existe un libro de ventas
        Libro.objects.create(empresa=self.empresa, tipo_libro="V")

        # Act: intentamos crear otro igual
        duplicado = Libro(empresa=self.empresa, tipo_libro="V")

        # Assert: tiene que quejarse
        with self.assertRaises(ValidationError):
            duplicado.full_clean()