from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse 

from .models import Empresa, Libro, CliPro, Detalle

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

class Vistastest(TestCase):
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
        self.cli_pro = CliPro.objects.create(
            nombre="Librería juvenil",
            direccion="Calle San Martín 1234",
            telefono="",
            cuit="30-12121212-0",
            es_cliente=False,
            es_proveedor=True,
            iva="I",
            obs="Librería"
        )
        self.libro = Libro.objects.create(
            empresa=self.empresa,
            tipo_libro="V"
        )
        self.detalle = Detalle.objects.create(
            libro=self.libro,
            fecha="2017-12-01",
            tipo_comprobante="F",
            letra="C",
            sucursal="1",
            nfactura="1",
            cli_pro=self.cli_pro,
            gravado="4356.00",
            no_gravado="0.00",
            iva21="0.00",
            iva105="0.00",
            iva_otros="0.00",
            rg2126="0.00",
            ret_IVA="0.00",
            ret_iibb="0.00",
            imp_int="0.00",
            otros="0.00"
        )

    def protected_views(self):
        return [
            ("iva:home", {}),
            ("iva:usuarios", {}),

            ("iva:a_empresa", {}),
            ("iva:exp_empresa", {}),
            ("iva:imp_empresa", {}),
            ("iva:l_empresa", {}),
            ("iva:m_empresa", {"id": self.empresa.id}),
            ("iva:v_empresa", {"id": self.empresa.id}),
            ("iva:d_empresa", {"id": self.empresa.id}),
            
            ("iva:a_cli_pro", {}),
            ("iva:exp_cli_pro", {}),
            ("iva:imp_cli_pro", {}),
            ("iva:l_cli_pro", {}),
            ("iva:m_cli_pro", {"id": self.cli_pro.id}),
            ("iva:v_cli_pro", {"id": self.cli_pro.id}),
            ("iva:d_cli_pro", {"id": self.cli_pro.id}),

            ("iva:a_libro", {"k": self.empresa.id, "v": "V"}),
            ("iva:i_libro", {"id": self.libro.id}),
            ("iva:m_libro", {"id": self.libro.id}),
            ("iva:v_libro", {"id": self.libro.id}),
            ("iva:d_libro", {"id": self.libro.id}),
            ("iva:l_libro", {}),

            ("iva:i_dgr", {"id": self.libro.id}),

            ("iva:a_detalle", {"l": self.libro.id}),
            ("iva:m_detalle", {"id": self.detalle.id}),
            ("iva:v_detalle", {"id": self.detalle.id}),
            ("iva:d_detalle", {"id": self.detalle.id}),
        ]

    def test_vistas_protegidas_devuelven_404_sin_login(self):
        for view_name, kwargs in self.protected_views():

            response = self.client.get(view_name, kwargs=kwargs)
            self.assertEqual(response.status_code, 404)

            # PARA HACER DESPUES:
            """
            self.assertEqual(response.status_code, 302)
            self.assertIn("/login", response.url)  # o LOGIN_URL

            """

       