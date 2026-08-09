# Libros IVA

Aplicación de gestión de **libros de IVA compras y ventas**: registra empresas, clientes y
proveedores, y genera los libros fiscales con exportación a PDF y a Excel. Construida con Django.

> ### 🔓 Datos de demostración
>
> Este repositorio incluye **datos ficticios** y un usuario de prueba:
>
> | Usuario | Contraseña |
> | ------- | ---------- |
> | `demo`  | `demo1234` |
>
> No contiene información real de ninguna empresa ni persona. La contraseña es pública a
> propósito, para que cualquiera pueda probar la aplicación.

---

## Uso diario

Si ya lo tenés instalado, ubicarse en la carpeta raíz del proyecto y luego son dos comandos:

```bash
source env/bin/activate
python manage.py runserver
```

Abrir **http://127.0.0.1:8000/** y entrar con `demo` / `demo1234`.

El menú principal está en `/home/` y el panel de administración de Django en `/admin/`.
Para parar el servidor: `Ctrl+C`. Dejá la terminal abierta mientras uses la app.

---

## Instalación desde cero

### Requisitos previos

- **Python 3.8.18**, instalado con [pyenv](https://github.com/pyenv/pyenv):
  ```bash
  pyenv install 3.8.18
  ```
- git

> **¿Por qué 3.8?** El proyecto usa Django 1.11, que oficialmente llega hasta Python 3.7 y en la práctica funciona en 3.8. Con un Python más nuevo **no arranca**.
>
> Por eso el entorno virtual se crea con el 3.8.18 de pyenv y no con el `python3` del sistema.
> Ver [Notas técnicas](#notas-técnicas).

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/caritodoer/hugoiva.git
cd hugoiva

# 2. Crear el entorno virtual con Python 3.8
~/.pyenv/versions/3.8.18/bin/python -m venv env

# 3. Activarlo
source env/bin/activate

# 4. Instalar las dependencias
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# 5. Crear el archivo de configuración
cp .env.example .env

# 6. Crear las tablas de la base de datos
python manage.py migrate

# 7. Cargar los datos de demostración
python manage.py loaddata datos_demo

# 8. Arrancar
python manage.py runserver
```

Abrir **http://127.0.0.1:8000/** y entrar con `demo` / `demo1234`.

### Sobre el archivo `.env`

La configuración sensible no está en el código, se lee de un archivo `.env` que **no se versiona**.
`.env.example` es la plantilla: copiala y ya funciona en local.

Para generar una clave de firma propia (recomendable si vas a trabajar sobre el proyecto):

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Y pegá el resultado en `DJANGO_SECRET_KEY` dentro de tu `.env`.

---

## Recuperación de posibles errores

### "La app no arranca: `ImproperlyConfigured: Falta la variable de entorno DJANGO_SECRET_KEY`"

No tenés archivo `.env`. Crealo desde la plantilla:

```bash
cp .env.example .env
```

Tiene que contener tres variables: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG` y `DJANGO_ALLOWED_HOSTS`.
Mirá `.env.example` para ver qué significa cada una.

### "No tengo la base de datos"

Los datos de demostración viven en el repositorio, en `IVAcompras/fixtures/datos_demo.json`. La base se reconstruye con dos comandos:

```bash
python manage.py migrate           # crea las tablas vacías
python manage.py loaddata datos_demo   # mete los datos
```

### "Quiero borrar la base de datos y dejarla como al principio"

```bash
rm db.sqlite3
python manage.py migrate
python manage.py loaddata datos_demo
```

### "Cambié los datos de demostración y quiero guardarlos en el repositorio"

```bash
python manage.py dumpdata IVAcompras auth.User --indent 2 --output IVAcompras/fixtures/datos_demo.json
```

> ⚠️ **Importante.** Ese comando exporta **todos** los usuarios de la base, con sus contraseñas
> cifradas. Si creaste algún usuario tuyo, abrí el JSON y borrá a mano los objetos con
> `"model": "auth.user"` que no sean `demo`, **antes de commitear**. En este repositorio solo
> debe publicarse el usuario de demostración.

### "No recuerdo la contraseña de un usuario"

```bash
python manage.py changepassword demo
```

### "`source: no such file or directory: env/bin/activate`"

El entorno virtual no existe o se rompió (pasa, por ejemplo, si desinstalás la versión de Python
con la que se creó). Se recrea así:

```bash
cd ~/Proyectos/hugoiva
rm -rf env
~/.pyenv/versions/3.8.18/bin/python -m venv env
source env/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### "`Error: That port is already in use`"

Ya hay un servidor corriendo. O usás el que está, o levantás otro en un puerto distinto:

```bash
python manage.py runserver 8001
```

Y abrís `http://127.0.0.1:8001/`.

### "`/home/` me devuelve 404"

No es un fallo: la aplicación responde 404 cuando no hay sesión iniciada. Entrá por
http://127.0.0.1:8000/ y logueate primero.

---

## Notas técnicas

- **Django 1.11.29 sobre Python 3.8.18.** El proyecto es de 2017 y nació con Django 1.10, que no
  arranca en ningún Python 3.6 o superior. Django 1.11 es la última versión compatible con las
  APIs que usa este código, y por eso está congelado ahí de momento.
- **`OLD_requirements.txt`** guarda los pines de dependencias originales de 2017. Varios ya no
  compilan en macOS con procesador Apple Silicon; `requirements.txt` documenta en su cabecera
  qué se cambió y por qué.

## Estructura

```
IVA/          configuración del proyecto (settings, urls, wsgi)
IVAcompras/   app principal: empresas, clientes/proveedores, libros y detalles
cuentas/      login, logout y registro de usuarios
templates/    plantillas HTML
static/       CSS, JavaScript e imágenes
locale/       traducciones
```

---

## Tests

Para correr los tests:

- `python manage.py test` (todo),
- `python manage.py test IVAcompras` (una app),
- `python manage.py test -v 2` (detalle de cada test).
