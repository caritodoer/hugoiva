"""
vistas:
- Cliente-Proveedor : Exportar, Importar, Listado, Alta, Modificar, Visualizar, Eliminar
- Empresas : Exportar, Importar, Listado, Alta, Modificar, Visualizar, Eliminar
- Libros : Listado, Alta, Modificar, Visualizar, Eliminar
- Detalle : Alta, Modificar, Visualizar, Eliminar
- Informes : Motor de PDF: Informe DGR, Informe Libro
- Usuarios : Listado
- Home : Inicio
"""

from .cliente_proveedor import (
    exp_cli_pro,
    imp_cli_pro,
    l_cli_pro,
    a_cli_pro,
    m_cli_pro,
    v_cli_pro,
    d_cli_pro,
)
from .detalle import a_detalle, m_detalle, v_detalle, d_detalle
from .empresa import (
    exp_empresa,
    imp_empresa,
    l_empresa,
    a_empresa,
    m_empresa,
    v_empresa,
    d_empresa,
)
from .home import home
from .informes import i_dgr, i_libro
from .libro import l_libro, a_libro, m_libro, v_libro, d_libro
from .users import usuarios

# API publica del paquete: los nombres que IVAcompras/urls.py espera encontrar
# como views.<nombre>. Declararlo evita que un linter marque los imports de
# arriba como "sin usar", y sirve de indice de lo que expone el paquete.
__all__ = [
    # Cliente-Proveedor
    "exp_cli_pro",
    "imp_cli_pro",
    "l_cli_pro",
    "a_cli_pro",
    "m_cli_pro",
    "v_cli_pro",
    "d_cli_pro",
    # Detalle
    "a_detalle",
    "m_detalle",
    "v_detalle",
    "d_detalle",
    # Empresa
    "exp_empresa",
    "imp_empresa",
    "l_empresa",
    "a_empresa",
    "m_empresa",
    "v_empresa",
    "d_empresa",
    # Home
    "home",
    # Informes (PDF)
    "i_dgr",
    "i_libro",
    # Libro
    "l_libro",
    "a_libro",
    "m_libro",
    "v_libro",
    "d_libro",
    # Usuarios
    "usuarios",
]
