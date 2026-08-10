from django.test import TestCase
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Empresa, Libro, CliPro, Detalle


# Create your tests here.
def vistas_de_lectura(caso_de_prueba):
    return [
        ("iva:home", {}),
        ("iva:usuarios", {}),
        ("iva:a_empresa", {}),
        ("iva:exp_empresa", {}),
        ("iva:imp_empresa", {}),
        ("iva:l_empresa", {}),
        ("iva:m_empresa", {"id": caso_de_prueba.empresa.id}),
        ("iva:v_empresa", {"id": caso_de_prueba.empresa.id}),
        ("iva:a_cli_pro", {}),
        ("iva:exp_cli_pro", {}),
        ("iva:imp_cli_pro", {}),
        ("iva:l_cli_pro", {}),
        ("iva:m_cli_pro", {"id": caso_de_prueba.cli_pro.id}),
        ("iva:v_cli_pro", {"id": caso_de_prueba.cli_pro.id}),
        ("iva:m_libro", {"id": caso_de_prueba.libro.id}),
        ("iva:v_libro", {"id": caso_de_prueba.libro.id}),
        ("iva:l_libro", {}),
        ("iva:a_detalle", {"l": caso_de_prueba.libro.id}),
        ("iva:m_detalle", {"id": caso_de_prueba.detalle.id}),
        ("iva:v_detalle", {"id": caso_de_prueba.detalle.id}),
        ("iva:i_libro", {"id": caso_de_prueba.libro.id}),
        ("iva:i_dgr", {"id": caso_de_prueba.libro.id}),
    ]


def vistas_que_modifican(caso_de_prueba):
    return [
        ("iva:a_libro", {"k": caso_de_prueba.empresa.id, "v": "C"}),
        ("iva:d_detalle", {"id": caso_de_prueba.detalle.id}),
        ("iva:d_libro", {"id": caso_de_prueba.libro.id}),
        ("iva:d_cli_pro", {"id": caso_de_prueba.cli_pro.id}),
        ("iva:d_empresa", {"id": caso_de_prueba.empresa.id}),
    ]


class DatosDePrueba(TestCase):
    def setUp(self):
        # Se ejecuta antes de CADA test, sobre una base vacía.
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

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
            obs="Librería",
        )
        self.libro = Libro.objects.create(empresa=self.empresa, tipo_libro="V")
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
            otros="0.00",
        )


class VistasTests(DatosDePrueba):
    def test_vistas_protegidas_devuelven_404_sin_login(self):
        allViews = vistas_de_lectura(self) + vistas_que_modifican(self)
        for view_name, kwargs in allViews:
            with self.subTest(vista=view_name):
                response = self.client.get(reverse(view_name, kwargs=kwargs))
                self.assertEqual(response.status_code, 404)

                # PARA HACER DESPUES:
                # self.assertEqual(response.status_code, 302)
                # self.assertIn("/login", response.url)  # o LOGIN_URL


class SmoketestTests(DatosDePrueba):
    def test_vistas_dan_200_cuando_estoy_logueado(self):
        self.client.force_login(self.user)

        for view_name, kwargs in vistas_de_lectura(self):
            with self.subTest(vista=view_name):
                response = self.client.get(reverse(view_name, kwargs=kwargs))
                self.assertEqual(response.status_code, 200)

        # for view_name, kwargs in vistas_que_modifican(self):
        #    with self.subTest(vista=view_name):
        #        response = self.client.get(reverse(view_name, kwargs=kwargs))
        #        self.assertEqual(response.status_code, 302)


class EmpresaTests(DatosDePrueba):
    def setUp(self):
        super().setUp()
        self.empresaDos = Empresa.objects.create(
            nombre="Segunda Empresa de prueba",
            propietario="Alguien más",
            cuit="20-22222222-2",
            localidad="Buenos Aires",
            direccion="Calle 2",
            directorio="prueba",
        )

    def test_get_absolute_url_apunta_al_detalle_de_la_empresa(self):
        self.assertEqual(
            self.empresa.get_absolute_url(), f"/v_empresa/{self.empresa.id}/"
        )

    def test_el_listado_muestra_las_empresas_existentes(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("iva:l_empresa"))
        self.assertContains(response, "Empresa de prueba")
        self.assertContains(response, "Segunda Empresa de prueba")

    def test_alta_de_empresa_y_redirige_a_la_vista_de_la_empresa(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("iva:a_empresa"),
            {
                "nombre": "Empresa BBB",
                "propietario": "Alguien",
                "cuit": "44-44444444-4",
                "localidad": "Córdoba",
                "direccion": "Calle 1",
                "directorio": "prueba",
            },
        )
        self.assertEqual(response.status_code, 302)
        newEmpresa = Empresa.objects.get(cuit="44-44444444-4")
        self.assertRedirects(
            response, reverse("iva:v_empresa", kwargs={"id": newEmpresa.id})
        )


class LibroTests(DatosDePrueba):
    def test_no_permite_dos_libros_de_ventas_en_la_misma_empresa(self):
        # ya existe un libro de ventas en el setup
        # intentamos crear otro igual
        duplicado = Libro(empresa=self.empresa, tipo_libro="V")

        # Assert: tiene que quejarse
        with self.assertRaises(ValidationError):
            duplicado.full_clean()


class E2E_LibroPdfTests(DatosDePrueba):

    def test_pdf_de_libro_se_genera_correctamente(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("iva:i_libro", kwargs={"id": self.libro.id}),
            {"d": "2017-12-01", "h": "2017-12-31"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertTrue(response.content.startswith(b"%PDF"))
        self.assertGreater(len(response.content), 0)


class DetalleTests(DatosDePrueba):
    def test_no_permite_dos_detalles_de_facturas_en_la_misma_empresa(self):

        # Act: intentamos crear otro igual
        duplicado = Detalle(
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
            otros="0.00",
        )

        # Assert: tiene que quejarse
        with self.assertRaises(ValidationError):
            duplicado.full_clean()
