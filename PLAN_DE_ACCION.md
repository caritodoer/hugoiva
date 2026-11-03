# Plan de acción — hugoiva

Checklist de trabajo para modernizar el proyecto. Sin fechas: avanzá al ritmo que quieras,
pero **respetá el orden de las fases**, porque cada una apoya en la anterior.

Estado del proyecto al escribir este plan: Django 1.11.29 sobre Python 3.8.18, funcionando.
Para levantarlo, ver la sección "Cómo lanzarlo" del `README.md`.

---

## Cómo usar este plan

**El trato: vos escribís el código, yo explico y reviso.** Este documento no trae soluciones
copiables a propósito. Trae objetivos, pistas y criterios para saber si lo lograste.

**Con una excepción: la Fase A va con comandos exactos.** Es fontanería de repositorio y
configuración, no es donde querés practicar Python ni diseño. Aun así, cada paso explica el
porqué: si querés entenderlo en vez de ejecutarlo, preguntame antes de copiar.

Cada tarea tiene esta forma:

- **Objetivo** — qué tiene que ser cierto cuando termines
- **Por qué** — qué problema real resuelve (si no te convence, discutímelo)
- **Pistas** — por dónde empezar a buscar, sin darte la respuesta
- **Hecho cuando** — cómo comprobás vos misma que está bien

### Cómo pedirme ayuda sin que te arruine el ejercicio

Frases que funcionan bien conmigo:

- _"Dame una pista sobre la tarea B3, no la solución"_
- _"Escribí esto, ¿qué le ves mal?"_ ← la mejor forma de aprender
- _"Explicame por qué Django hace X de esta manera"_
- _"Estoy atascada hace rato en B5, ahora sí mostrame cómo se hace y explicámelo"_ ← totalmente válido,
  pelearte 40 minutos con algo enseña, pelearte 3 horas solo frustra

Frases que te van a robar el aprendizaje (evitalas salvo que sea a propósito):

- _"Hacelo vos"_ en tareas de las fases B, C y D

### Reglas de higiene mientras trabajás

- [ ] Trabajá en ramas, no en `master`: una rama por fase (`fase-a-seguridad`, `fase-b-limpieza`, …)
- [ ] Commits chicos y con mensaje descriptivo. Nada de `mejoras` ni `10-12-17`
      (mirá `git log` para ver por qué te lo digo)
- [ ] Después de cada cambio, **abrí la app en el navegador y probá la pantalla que tocaste**.
      No hay tests todavía que te avisen si rompiste algo
- [ ] Si algo se rompe y no entendés por qué: `git diff` antes de tocar nada más

---

## FASE A — Higiene del repositorio ✅ COMPLETADA

> **Hecha por Claude**, a pedido tuyo, en la rama `refactor` (commit `46280c0`). Es fontanería,
> no práctica. Queda documentada abajo por si necesitás entender qué se hizo o repetirlo.
>
> **Variante sobre lo planificado:** en vez de cambiar las contraseñas de `admin` y `carito`
> (paso A1), elegiste **borrar esas dos cuentas**. La base local tiene ahora un único usuario,
> `demo` / `demo1234`, documentado en el README.
>
> **Lo único que queda de tu lado:** si la contraseña de `admin` o de `carito` la usabas también
> en tu correo, tu GitHub o cualquier otro sitio, cambiala **ahí**. Las cuentas ya no existen,
> pero sus hashes siguen en el historial de commits antiguos, y ese riesgo solo se cierra
> donde reutilizaste la contraseña.

**El objetivo real de esta fase no es "seguridad".** Este proyecto no va a producción y querés
que cualquiera lo clone y lo ejecute: eso está bien y el plan lo respeta. Lo que buscamos es que
el repo contenga **datos de demo públicos y reproducibles** en vez de tus datos personales, y que
la configuración se vea profesional para quien entre a mirar cómo trabajás.

De todo esto, **solo el paso A1 es urgente de verdad**. El resto es oficio.

> **Esta fase va con comandos exactos**, porque es fontanería y no es donde querés practicar.
> Las fases B, C y D siguen en modo pistas. Todos los comandos asumen el entorno activado:
> `cd ~/Proyectos/hugoiva && source env/bin/activate`

> **Documentá sobre la marcha.** Al terminar cada paso, escribí en el README lo que acabás de
> hacer. El paso A7 dice exactamente qué secciones tiene que tener, pero no lo dejes para el
> final: lo que hoy te parece obvio, en seis meses no lo va a ser. Ese README es tu red de
> seguridad, no un trámite.

### A1. Cambiar tus contraseñas reales

- **Objetivo:** que ninguna contraseña tuya siga publicada, ni siquiera en forma de hash.
- **Por qué:** es lo único con riesgo real de toda la fase. Los hashes de `admin` y `carito` están
  en GitHub con configuración de 2017 (PBKDF2 con 30.000 y 36.000 iteraciones; Django 5 usa más de
  un millón). Se pueden atacar **offline**, sin tocar ningún servidor. Si esas contraseñas eran
  cortas o comunes, se sacan. El peligro no es esta app: es que la misma contraseña te sirva
  para entrar a tu correo o a tu GitHub.

```bash
python manage.py changepassword admin
python manage.py changepassword carito
```

- **Y lo más importante:** si alguna de esas dos contraseñas la usabas en otro sitio, cambiala
  también ahí. Ese es el paso que de verdad cierra el riesgo.
- **Hecho cuando:** entrás con las nuevas y no reutilizás la vieja en ningún lado.

### A2. Crear el usuario de demo

- **Objetivo:** un usuario cuya contraseña es pública **a propósito**, para que cualquiera pruebe la app.
- **Por qué:** así el visitante entra sin fricción y vos no publicás nada tuyo. Una contraseña
  que se publica en el README no es una filtración: es documentación.

```bash
python manage.py createsuperuser
```

Te va a pedir tres cosas. Usá exactamente esto (o lo que prefieras, pero anotalo):

- Username: `demo`
- Email: podés dejarlo vacío
- Password: `demo1234`

Django va a protestar diciendo que la contraseña es demasiado común y te va a preguntar si querés
usarla igualmente: respondé que sí (`y`). Es justo lo que buscamos.

- **Hecho cuando:** podés entrar en la app con `demo` / `demo1234`.

### A3. Exportar los datos de demo a un fixture

- **Objetivo:** un archivo JSON versionado que contiene los datos de ejemplo y el usuario `demo`.
- **Por qué:** es la pieza que te permite borrar la base binaria del repo sin perder nada.
  El JSON es texto: git te muestra en el diff qué dato cambió, y podés reconstruir la base en
  cualquier ordenador. Un _fixture_ es eso: datos guardados en un archivo que Django sabe cargar.

Primero creá la carpeta donde Django los busca por convención:

```bash
mkdir -p IVAcompras/fixtures
```

Ahora exportá los datos de la app **y** los usuarios:

```bash
python manage.py dumpdata IVAcompras auth.User --indent 2 --output IVAcompras/fixtures/datos_demo.json
```

**Paso importante:** ese archivo ahora contiene también a `admin` y `carito`, con sus hashes
nuevos. No los queremos publicar. Abrilo en el editor, buscá los bloques cuyo `"model"` sea
`"auth.user"` y **borrá a mano los objetos de `admin` y `carito`**, dejando solo el de `demo`.

Es un JSON: cada objeto va entre llaves dentro de la lista. Cuidá que después de borrar sigan
bien las comas entre elementos. Si te queda mal, el paso A4 te lo va a decir enseguida.

- **De paso, mirá el archivo con calma.** Ver tus modelos serializados a JSON enseña bastante
  sobre cómo Django representa los datos internamente.
- **Hecho cuando:** el JSON tiene un solo usuario (`demo`) y tus empresas, clientes y libros.

### A4. Comprobar que el fixture reconstruye la base desde cero

- **Objetivo:** demostrarte a vos misma que podés borrar `db.sqlite3` sin perder nada.
- **Por qué:** es exactamente lo que te preocupaba al cambiar de ordenador. Mejor comprobarlo
  ahora, con una copia de seguridad al lado, que descubrirlo el día que haga falta.

```bash
mv db.sqlite3 db.sqlite3.backup
python manage.py migrate
python manage.py loaddata datos_demo
python manage.py runserver
```

Entrá a http://127.0.0.1:8000/ con `demo` / `demo1234` y revisá que estén tus empresas,
clientes y libros.

- **Si funcionó:** ya podés borrar la copia (`rm db.sqlite3.backup`). Acabás de probar que
  cualquiera puede clonar el repo y tener la app poblada con dos comandos.
- **Si falló:** restaurá con `mv db.sqlite3.backup db.sqlite3` y revisá el JSON del paso A3
  (lo más habitual es una coma de más o de menos al borrar los usuarios).
- **Fijate en el orden:** `migrate` crea las tablas vacías, `loaddata` mete los datos. Son dos
  cosas distintas y esa distinción te va a servir siempre.
- **Hecho cuando:** reconstruiste la base desde cero y la app funciona igual.

### A5. Sacar del repo lo que no es código fuente

- **Objetivo:** `db.sqlite3` y `static_root/` dejan de estar versionados.
- **Por qué:** la base ya no hace falta (la reconstruís con A4) y además te ensucia el
  `git status` cada vez que usás la app — ya te pasó, el commit `2f45a65 "Update db.sqlite3"`
  es justo eso. Y `static_root/` son archivos **generados** por `collectstatic`: versionar algo
  que se regenera con un comando es duplicar.

Añadí estas dos líneas al final del `.gitignore`:

```
db.sqlite3
static_root/
```

Y decile a git que deje de rastrearlos **sin borrarlos del disco** (eso hace `--cached`):

```bash
git rm --cached db.sqlite3
git rm -r --cached static_root
```

- **Ojo:** esto corta la exposición de acá en adelante, pero los archivos **siguen en el historial**
  de commits anteriores. Limpiar el pasado requiere reescribir la historia (`git filter-repo`) y
  no hace falta en tu caso: los hashes que había ahí ya los invalidaste en A1.
- **Hecho cuando:** `git status` ya no menciona `db.sqlite3` aunque uses la app, y los archivos
  siguen existiendo en tu carpeta.

### A6. Configuración por variables de entorno

- **Objetivo:** `SECRET_KEY` y `DEBUG` se leen del entorno, no están cableados en `settings.py`.
- **Por qué:** en tu caso **no es seguridad**, es señal profesional. Tu repo es público justamente
  para que vean cómo trabajás: quien lo abra y encuentre configuración por entorno lee "sabe cómo
  se despliega una aplicación". Si encuentra la clave escrita a mano, lee lo contrario.

Instalá la librería que lee archivos `.env`:

```bash
pip install python-dotenv==1.0.1
```

Añadila a `requirements.txt` (a mano, respetando el orden alfabético del archivo).

Ahora te tocan tres ediciones en `IVA/settings.py`. **Acá sí te dejo trabajar**, porque es Python
y es donde querés practicar:

1. Cargar el `.env` al principio del archivo. La librería se usa con `from dotenv import load_dotenv`
   y luego llamando a `load_dotenv()`. Tiene que ejecutarse **antes** de leer cualquier variable.
2. `SECRET_KEY` pasa a leerse con `os.environ` (el módulo `os` ya está importado en la línea 15).
   Investigá la diferencia entre `os.environ.get("X")` y `os.environ["X"]`: uno devuelve `None`
   en silencio si falta y el otro falla ruidosamente. Para una clave que la app necesita sí o sí,
   pensá cuál de los dos comportamientos preferís.
3. `DEBUG` igual, pero con una trampa clásica: las variables de entorno **siempre son strings**.
   Probá `bool("False")` en el shell de Python y vas a ver por qué no podés convertir directamente.

Creá tu archivo `.env` en la raíz (ya está en `.gitignore`, línea 76, así que no se sube):

```
DJANGO_SECRET_KEY=poné-acá-una-clave-larga-y-aleatoria
DJANGO_DEBUG=True
```

Para generar una clave nueva, Django trae una utilidad:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Y creá también un `.env.example` **con el mismo contenido pero una clave de ejemplo**, este sí
versionado. Es lo que le dice al visitante qué variables necesita: copia el archivo, y listo.

- **Nota:** dejá `DJANGO_DEBUG=True` en tu `.env`. Para un proyecto de demo local, la página de
  error detallada de Django es una ventaja, no un problema.
- **Hecho cuando:** `grep SECRET_KEY IVA/settings.py` no muestra ninguna clave literal, la app
  arranca, y probaste qué pasa si borrás la variable del `.env` (el error debería ser claro).

### A7. Documentar todo en el README

- **Objetivo:** que el `README.md` alcance para dos personas distintas: alguien que clona el repo
  por primera vez, **y vos dentro de seis meses**, cuando no te acuerdes de nada de esto.
- **Por qué:** sin este paso, los seis anteriores no sirven. Y el segundo lector es el más
  importante: hoy sabés qué es un fixture y para qué sirve el `.env` porque acabás de hacerlo.
  En marzo no. Escribí para esa persona.

**Regla de oro: no dejes esto para el final.** Cada vez que termines un paso de la A1 a la A6,
anotá en el README lo que acabás de hacer, mientras lo tenés fresco. Documentar de memoria una
semana después es cuando se cuelan los pasos olvidados.

La sección "Cómo lanzarlo" que hay hoy en el README quedó obsoleta con esta fase: reemplazala.
Y borrá la sección de instalación de 2017 del final del archivo, que dice `pip install django==1.10`
y ya no aplica.

#### Estructura que tiene que tener el README

**1. Qué es esto**
Una o dos frases: qué problema resuelve la app y para quién. Que alguien sepa en diez segundos
si le interesa seguir leyendo.

**2. Aviso de datos de demostración**
Bien arriba y bien visible:

> **Datos de demostración.** Este repositorio incluye datos ficticios y un usuario de prueba:
> `demo` / `demo1234`. No contiene información real.

**3. Requisitos previos**
Qué necesita tener instalado antes de empezar: Python 3.8.18 y cómo conseguirlo con pyenv
(`pyenv install 3.8.18`), y git. Decí explícitamente **por qué 3.8 y no el Python del sistema**,
o el primero que lo intente con su Python nuevo se va a estrellar sin entender nada.

**4. Instalación desde cero**
La secuencia completa, en bloques de código copiables, sin pasos implícitos:

1. `git clone` y entrar a la carpeta
2. Crear el entorno virtual con el Python 3.8 de pyenv
3. Activarlo
4. `pip install -r requirements.txt`
5. `cp .env.example .env` — y **explicar que hay que generar un `SECRET_KEY` propio**, con el
   comando exacto que usaste en A6
6. `python manage.py migrate`
7. `python manage.py loaddata datos_demo`
8. `python manage.py runserver`
9. Abrir http://127.0.0.1:8000/ y entrar con las credenciales de demo

**5. Uso diario**
Los tres comandos para arrancar cuando ya está todo instalado (`cd`, `source`, `runserver`),
y cómo parar el servidor. Separado de la instalación, porque es lo que vas a mirar el 95% de las veces.

**6. Recuperación — "se me rompió algo"**
Esta es la sección que te va a salvar a vos, no al visitante. Un apartado por síntoma, con el
síntoma como título para poder encontrarlo rápido:

- **"Perdí el `.env`" o "la app no arranca por falta de SECRET_KEY"** → copiar de nuevo
  `.env.example`, generar una clave con el comando de A6, y qué variables tiene que contener
- **"Perdí la base de datos" / "la borré" / "cambié de ordenador"** → `migrate` + `loaddata datos_demo`.
  Dejá claro que **no se pierde nada**, que los datos de demo viven en el fixture
- **"Quiero volver a dejar la base como estaba al principio"** → borrar `db.sqlite3` y repetir lo anterior
- **"Cambié los datos de demo y quiero guardarlos en el repo"** → el comando `dumpdata` de A3,
  **con el recordatorio de quitar del JSON los usuarios que no sean `demo`**. Este es el que más
  fácil se olvida y el que peores consecuencias tiene
- **"No recuerdo la contraseña"** → `python manage.py changepassword <usuario>`
- **"`source: no such file or directory: env/bin/activate`"** → recrear el entorno virtual (ya está
  escrito en el README actual, conservalo)
- **"`That port is already in use`"** → usar otro puerto (ya está escrito, conservalo)

**7. Notas técnicas**
Por qué Django 1.11 y Python 3.8, y qué es `OLD_requirements.txt`. Mencioná que hay un plan de
migración a Django 5.x en `PLAN_DE_ACCION.md`. Esto le dice a quien revise que las versiones
viejas son una decisión consciente y documentada, no descuido.

> Las capturas de pantalla y la parte de "decisiones de diseño" van en la **Fase E**, cuando ya
> tengas el rediseño hecho. Ahora ocupate solo de que el README funcione como manual.

#### Cómo comprobar que está completo

Esto no es opcional, es la única forma de saberlo:

```bash
cd /tmp
git clone ~/Proyectos/hugoiva prueba-readme
cd prueba-readme
```

**Commiteá antes de hacer esto.** `git clone` copia solo lo que está commiteado: si el fixture o
el `.env.example` siguen sin commitear, la copia no los va a tener y vas a estar depurando un
problema que no existe. Y fijate en algo importante: en esa carpeta **no** va a estar tu `.env`
ni tu `db.sqlite3`, porque los ignoraste en A5 y A6. Eso es exactamente lo que queremos probar —
que se pueden reconstruir desde cero siguiendo el README.

Y ahora seguí tu propio README **al pie de la letra**, sin usar nada que sepas de memoria.
Cada vez que tengas que improvisar algo que no está escrito, volvé y añadilo.

- **Hecho cuando:** levantaste la app en esa carpeta nueva siguiendo solo el README, sin improvisar
  ni una vez. Después podés borrarla (`rm -rf /tmp/prueba-readme`).

---

## FASE B — Higiene del código Python

Acá es donde vas a recuperar Python y Django. Ninguna tarea es difícil; todas te obligan a
entender cómo piensa el framework. **No pases a la Fase C sin terminar esta**: vas a tocar
las mismas vistas cuando rediseñes, y conviene que ya estén limpias.

### B1. Reemplazar los 32 chequeos de login manuales

- **Objetivo:** ninguna vista vuelve a escribir `if not request.user.is_authenticated(): raise Http404`.
- **Por qué:** está copiado **32 veces** entre `IVAcompras/views.py` y `cuentas/views.py`. Si mañana
  querés cambiar el comportamiento (redirigir al login en vez de dar 404), hoy tenés que editar
  32 sitios y no fallar en ninguno. Django resuelve esto desde hace más de una década.
- **Pistas:** buscá "decoradores" en la documentación de autenticación de Django. Antes de usarlo,
  entendé qué es un decorador en Python puro: es solo una función que envuelve a otra. Si nunca
  escribiste uno, escribí uno de juguete en el shell (que imprima "entrando"/"saliendo" alrededor
  de una función) — te va a hacer clic.
- **Decisión de diseño que tenés que tomar vos:** hoy un usuario no logueado recibe **404**
  (`raise Http404`). El decorador de Django, en cambio, **redirige al login**. Son experiencias
  muy distintas. ¿Cuál querés? Pista: pensá qué le pasa hoy a alguien que guardó `/l_empresa/`
  en favoritos y vuelve al día siguiente.
- **Cuidado:** si elegís redirigir, Django necesita saber a dónde. Buscá `LOGIN_URL` en settings
  y fijate cómo se relaciona con los nombres de tus rutas en `IVA/urls.py`.
- **Hecho cuando:** `grep -rn "is_authenticated" IVAcompras cuentas` devuelve muy pocas líneas
  (alguna puede quedar legítimamente, por ejemplo en `cuentas/views.py:login_view`), y probaste
  a mano que entrar sin sesión a `/l_empresa/` hace lo que decidiste.

### B2. Eliminar los `print()` de depuración

- **Objetivo:** cero `print()` en el código de vistas.
- **Por qué:** hay **16**. El de `IVAcompras/views.py:198` vuelca un diccionario entero a la
  consola en cada carga del home. En un servidor real esto ensucia los logs y puede filtrar datos.
- **Pistas:** algunos los vas a borrar sin más. Otros te estaban dando información útil: para esos,
  investigá el módulo `logging` de Python y la configuración `LOGGING` de Django. La diferencia
  clave: un `print` siempre imprime, un log tiene **nivel** y podés silenciarlo por entorno.
- **Hecho cuando:** `grep -rn "print(" IVAcompras cuentas` está limpio y la consola del `runserver`
  no escupe diccionarios al navegar.

### B3. Arreglar la vista rota `l_detalle`

- **Objetivo:** `/l_detalle/` deja de reventar.
- **Por qué:** la vista existe (`IVAcompras/views.py:730`), la URL existe (`IVAcompras/urls.py`),
  pero la plantilla `l_detalle.html` **no existe**. Entrar ahí lanza `TemplateDoesNotExist`.
  Ya lo verifiqué: está roto hoy.
- **Pistas:** primero investigá si esa vista se usa desde algún lado (buscá `l_detalle` en
  `templates/`). Si nadie la enlaza, quizá la respuesta correcta no sea crear la plantilla sino
  **borrar la vista y su URL**. Borrar código muerto es una decisión de ingeniería tan válida
  como escribirlo, y este proyecto tiene bastante.
- **Hecho cuando:** o `/l_detalle/` responde bien, o ya no existe la ruta. Sin puntos intermedios.

### B4. Limpiar plantillas y código huérfanos

- **Objetivo:** el repo no tiene archivos que no usa nadie.
- **Por qué:** `templates/pruebas.html` no lo renderiza ninguna vista. `templates/a_cp_modal.html`
  solo lo usa código comentado (`IVAcompras/views.py:676`). Hay bloques comentados grandes en
  `views.py`, `urls.py` y `templates/includes/menu.html`. El código comentado es ruido: git ya
  guarda el pasado por vos.
- **Pistas:** antes de borrar, confirmá que nadie lo usa (`grep` es tu amigo). Hacelo en un commit
  separado y solo de borrados, así es fácil de revertir si te equivocaste.
- **Hecho cuando:** la app funciona igual con menos archivos y menos líneas.

### B5. Eliminar los imports con asterisco

- **Objetivo:** ningún `from X import *` en el proyecto.
- **Por qué:** `IVAcompras/views.py` hace `from .models import *` y `from .forms import *`.
  Cuando leés `Empresa` en la línea 240, no hay forma de saber de dónde sale sin adivinar.
  Peor: si dos módulos definen el mismo nombre, uno pisa al otro en silencio. Es de los primeros
  puntos que mira alguien revisando tu código.
- **Pistas:** hacelo módulo por módulo. Un truco: comentá el import con asterisco y dejá que los
  errores te vayan diciendo qué nombres faltan. Si usás VS Code, el editor te los marca solo.
- **Hecho cuando:** los imports son explícitos y todas las pantallas siguen cargando.

### B1–B5 ✅ COMPLETADAS

Verificado: las 27 vistas de `IVAcompras/views.py` llevan decorador y **ninguna quedó sin
proteger**; con sesión las 24 rutas responden 200, sin sesión las protegidas dan 404. Cero
`print()`. `l_detalle` eliminada. `pruebas.html` y `a_cp_modal.html` borrados. Ningún `import *`
en el proyecto. `views.py` bajó de 745 a 651 líneas.

Además, por encima de lo planificado:

- El decorador vive en `cuentas/decorators.py`, no dentro de un módulo de vistas — que es
  donde corresponde, y así ambas apps lo importan sin dependencias raras
- Usa `is_authenticated` sin paréntesis, sin aviso de deprecación
- `models.py` ya importa `reverse` desde `django.urls`
- Resuelto el conflicto de nombres entre `datetime.time` y el módulo `time`
- `/register/` protegido: crear usuarios exige sesión

Flecos menores, para cuando pases por ahí (ninguno rompe nada):

- [ok] 3 imports sin usar en `views.py`, los tres huérfanos de mudar el decorador a
  `cuentas/decorators.py`: `Http404` (línea 4), `datetime` (línea 8) y `wraps` (línea 9)
- [ok] 4 imports de crispy sin usar en `forms.py:4`: `StrictButton`, `FieldWithButtons`,
  `PrependedAppendedText`, `FormActions`

### B6. Primeros tests — 2 de 7 hechos

- **Objetivo:** siete tests. Ni uno más: no busques cobertura total, buscá que te avisen
  cuando rompas algo importante.
- **Por qué:** los necesitás **antes de la Fase D**. Vas a reescribir 19 plantillas, y las vistas
  les pasan variables de contexto que ellas consumen: sin tests, la única forma de detectar que
  rompiste algo es abrir las 19 pantallas a mano después de cada cambio. También son
  imprescindibles para la Fase F (migración) y para B7.
- **Dónde van:** `IVAcompras/tests.py` y `cuentas/tests.py`.

| #   | Nivel       | Qué comprueba                                                                       | Estado       |
| --- | ----------- | ----------------------------------------------------------------------------------- | ------------ |
| 1   | Unit        | No se pueden crear dos libros del mismo tipo para la misma empresa                  | ✅ hecho     |
| 2   | Unit        | `Empresa.get_absolute_url()` devuelve `/v_empresa/<id>/`                            | ✅ hecho     |
| 3   | Integración | **Sin sesión, las vistas protegidas dan 404**                                       | ⬜ pendiente |
| 4   | Integración | El listado de empresas muestra las que existen                                      | ⬜ pendiente |
| 5   | Integración | POST a `a_empresa` crea el registro y redirige                                      | ⬜ pendiente |
| 6   | Integración | Login con credenciales correctas lleva a `/home`                                    | ⬜ pendiente |
| 7   | E2E         | Login → libro con detalles → PDF de `i_libro` con mes y año → responde PDF no vacío | ⬜ pendiente |

#### Test 3 — el imprescindible

- **Por qué es el más importante:** acabás de poner el decorador en 27 vistas a mano. Si algún día
  añadís una vista nueva y olvidás decorarla, **no da ningún error**: da una página que se ve
  perfecta y que cualquiera puede abrir sin sesión. Este test convierte esa comprobación en
  permanente.
- **Pistas:** una lista con las rutas protegidas y un bucle que compruebe el código de respuesta.
  Usá `self.client`, que ya viene incluido en `TestCase` — sin sesión iniciada, claro.
  Para las rutas con id (`/v_empresa/<id>/`), construilas con los objetos que creaste en `setUp`.
- **Hecho cuando:** el test falla si le quitás el decorador a una vista cualquiera. Probalo:
  quitá uno, mirá el fallo, y volvé a ponerlo. Un test que nunca viste fallar no sabés si funciona.

#### Tests 4, 5 y 6 — las vistas

- **Pistas:** `assertContains` (busca texto en la respuesta), `assertRedirects` (comprueba a dónde
  te manda) y `assertTemplateUsed`. Con esos tres cubrís los tres tests.
- Para el 4, creá dos empresas en `setUp` y comprobá que sus nombres aparecen en el listado.
- Para el 5, acordate de que un POST necesita un diccionario con **todos** los campos obligatorios
  del formulario. Comprobá las dos cosas: que el registro existe en la base después, y que
  la respuesta redirige.
- Para el 6, creá el usuario dentro del test con `create_user` (ojo: `User.objects.create()` guarda
  la contraseña sin cifrar y el login fallará; buscá la diferencia entre los dos métodos).

#### Test 7 — el end-to-end

- **Qué cubre:** es la razón de existir de la app. Si esto funciona, la aplicación cumple su
  propósito aunque todo lo demás esté feo.
- **Pistas:** el escenario necesita empresa + libro + al menos un detalle **con fecha**, porque
  `i_libro` filtra por mes y año que llegan como parámetros GET (`?m=...&a=...`). Fijate en la
  vista para ver los nombres exactos de esos parámetros antes de escribir el test.
- **Qué comprobar:** código 200, que la cabecera `Content-Type` sea `application/pdf`, y que el
  contenido no esté vacío. No intentes verificar el contenido del PDF: eso es un agujero sin fondo.

#### Tres cosas a las que prestar atención

- **La base de datos de test está vacía.** Django crea una base nueva, la destruye al terminar, y
  **tus datos de demo no están ahí**. Por eso cada clase crea lo suyo en `setUp`. Podés cargar el
  fixture con `fixtures = ['datos_demo']`, pero es mejor que cada test se construya su escenario:
  si mañana cambiás el fixture, no querés que se caigan diez tests.
- **En el `assert`, no uses el mismo mecanismo que usa el código.** Comprobar `reverse(...)` contra
  `reverse(...)` da un test que no puede fallar nunca. Escribí el resultado esperado a mano.
- **No testees a Django.** Que el ORM guarde un registro ya está probado por ellos. Testeá _tus_
  reglas: tus restricciones, tus vistas, tus permisos.

- **Cómo ejecutarlos:** `python manage.py test` (todo), `python manage.py test IVAcompras`
  (una app), `python manage.py test -v 2` (detalle de cada test).
- **Hecho cuando:** los siete pasan en verde, y viste fallar al menos al número 3 a propósito.

### B7. Partir `views.py`

- **Objetivo:** ningún archivo de vistas supera las ~250 líneas.
- **Por qué:** `IVAcompras/views.py` tiene **745 líneas y 28 funciones** que mezclan CRUD, generación
  de PDF con reportlab e importación de Excel. Encontrar algo ahí es un ejercicio de scroll.
- **Pistas:** una carpeta `views/` con `__init__.py` puede reemplazar a un archivo `views.py`
  (entendé por qué antes de hacerlo: qué es un paquete en Python). Un corte natural sería separar
  la generación de PDF, que es lo más voluminoso y lo menos relacionado con el resto.
  **Hacelo al final de la fase**, cuando ya tengas los tests de B6 avisándote si rompés algo.
- **Cuidado:** `IVA/urls.py` e `IVAcompras/urls.py` importan estas vistas. Si movés cosas, ajustá.
- **Hecho cuando:** los tests siguen pasando y podés explicar en una frase qué hay en cada archivo.

---

## FASE C — Sistema de diseño

Antes de tocar una sola pantalla, definí el vocabulario visual. Si vas pantalla por pantalla
improvisando, terminás con quince estilos distintos y eso es exactamente lo que hoy hace que
el proyecto parezca viejo.

**El diseño lo hacés vos.** Yo no voy a proponerte paletas ni tipografías. Lo que sigue son
las decisiones que tenés que tomar y los errores en los que suele caer la gente.

> **Las decisiones ya tomadas para esta fase** (el razonamiento completo está en
> `NOTAS_FASE_C.md`, leelo antes de empezar):
>
> | Pregunta                                | Decisión                                     |
> | --------------------------------------- | -------------------------------------------- |
> | ¿Tailwind o CSS crudo?                  | **CSS crudo** con custom properties          |
> | ¿Alguna librería de componentes?        | **Ninguna.** Open Props solo como referencia |
> | ¿Qué hacemos con crispy_forms?          | **Se saca.** Formularios a mano              |
> | ¿Cuándo se borra `bootstrap_modif.css`? | **En D8, no antes** (ver el aviso de abajo)  |

> ### ⚠️ Aviso de secuencia: qué se borra ahora y qué no
>
> **`bootstrap_modif.css` no se borra en esta fase.** Las 17 plantillas siguen llenas de
> `class="container"`, `col-md-10`, `btn btn-default`, `glyphicon-chevron-left`. El día que
> quites esa hoja, todas se caen a la vez.
>
> El orden correcto es: primero las plantillas dejan de usar clases de Bootstrap (Fase D, una
> pantalla por vez, con la app funcionando en cada paso), y **al final** se borra la hoja y se
> comprueba que no pasó nada. Eso es D8.
>
> En la Fase C sale todo lo que se puede quitar **sin romper nada visible**: la app
> `bootstrap3` (que está muerta), crispy (porque bloquea el diseño de los formularios),
> jQuery UI y el jQuery duplicado.

---

### C0. Preparar el terreno

- **Objetivo:** arrancar el rediseño desde un `master` sano y con el "antes" ya capturado.
- **Por qué:** el rediseño es lo único irreversible de todo el plan. Una vez que toques el CSS,
  no hay forma de volver a ver cómo se veía la app en 2017.

- [ ok] Mergear la rama `refactor` a `master` (son 13 commits, todo el trabajo de la Fase B)
- [ ok] Crear la rama de esta fase: `refactor-redesign`
- [ ok] **Sacar las capturas del estado actual**, a dos anchos: **1440 px y 360 px**
- [ ok] Guardarlas en una carpeta `screenshots/` con nombres que se entiendan
  (`home-1440.png`, `home-360.png`…)
- [ ok] capturas en gitignore

- **Sobre las capturas de 360 px:** son las que mejor van a contar el "antes y después",
  porque el menú móvil hoy está roto (el typo `data-toggle="collpase"` de D2). Eso se ve.
- **Sobre la captura del login:** sacala **tal como está hoy, rota** (ver C1). Es material
  honesto para el portfolio, no un descuido.
- **Hecho cuando:** `git log` en `master` muestra la Fase B completa, estás parada en
  `refactor-redesign`, y tenés las capturas commiteadas.

### C1. Auditar lo que hay

- **Objetivo:** saber exactamente qué CSS y qué JS se está cargando, y cuánto de eso usás.
- **Por qué:** hoy `base.html` carga cuatro hojas: `bootstrap_modif.css` (**6.761 líneas**),
  `iva.css` (154), `font-awesome.css` y `jquery-ui.css`. Antes de reescribir, entendé qué
  estás borrando.

- [ok] Pasar la pestaña **Coverage** de las DevTools de Chrome por el home, un listado y un
  formulario. Anotá el porcentaje de uso real de cada hoja
- [ok ] Anotar qué aporta cada hoja y cuál pensás eliminar
- [ ] Comprobar el bug del login (abajo) y **sacarle la captura antes de arreglarlo**
- [ ] Listar qué hace realmente el JS de `base.html` y de cada plantilla

- **Pistas:** con Coverage te vas a llevar una sorpresa con Bootstrap. Para el JS, buscá
  `$(` y `datepicker` en `templates/`.

#### Cuatro cosas ya verificadas, para que no las busques

1. **La pantalla de login carga una hoja que no existe.** `login_form.html:10` y
   `logout_form.html:10` enlazan `/static/css/bootstrap.css`. Ese archivo **no está en
   `static/`** — solo en `static_root/`, que es la salida de `collectstatic` y que sacaste del
   repo en A5. Comprobado levantando el servidor: `bootstrap.css` → **404**,
   `bootstrap_modif.css` → 200. O sea, **la primera pantalla que ve cualquiera está rota**
   desde antes de que empezaras, y en un clon nuevo se ve sin estilos.
2. **`iva2.css` sí lo carga alguien:** `login_form.html:11`. (El anexo de este plan decía que
   no lo cargaba nadie. Estaba mal, ya está corregido.)
3. **`login_form.html` y `logout_form.html` no heredan de `base.html`.** Son documentos HTML
   completos con su propio `<head>` duplicado — y con los mismos tres problemas que C7 arregla
   en `base.html`. Tenés que decidir si los pasás a `{% extends %}` o los dejás sueltos.
   Recomendación: heredar. Un `<head>` correcto escrito una vez es mejor que tres copias.
4. **Queda un modal muerto en `altas.html`** (líneas 15-29): `#acpmodal` con el cuerpo vacío,
   y el JS de la línea 41 engancha un click a `#btnguardar`, que **no existe en ninguna
   parte**. Son los restos de `a_cp_modal.html`, la plantilla que borraste en B4.

- **Hecho cuando:** podés decir qué hoja aporta qué, cuáles pensás eliminar, y tenés la
  captura del login roto.

### C2. Entender las custom properties y mirar Open Props

> La excepción que sí vale la pena mirar: Open Props. No es una librería de componentes, son literalmente custom properties de CSS: escalas de espaciado, tipografía, sombras, colores, curvas de animación. Cero componentes, cero opinión sobre cómo se ve un botón. Mi sugerencia no es que lo instales, sino que lo abras y le mires las escalas mientras hacés C2. Es una referencia excelente de cómo alguien que sabe construye una escala tipográfica o de sombras. Copiás el criterio, no el archivo.

- **Objetivo:** entender el mecanismo con el que vas a construir todo lo demás, y ver un
  ejemplo bien hecho antes de inventar el tuyo.
- **Por qué:** esta tarea no produce ningún archivo. Es media hora de leer que te va a ahorrar
  rehacer los tokens dos veces.

#### Qué son las custom properties

Una **custom property** (también llamada "variable CSS") es un valor con nombre que declarás
una vez y reutilizás en todo el CSS. Se declaran con dos guiones y se leen con `var()`:

```css
:root {
  --color-acento: #2563eb;
  --espacio-3: 12px;
}

.boton {
  background: var(--color-acento);
  padding: var(--espacio-3);
}
```

Tres cosas que las hacen distintas de las variables de Sass o Less, y que son justo las que
las convierten en la base de un sistema de diseño:

1. **Existen en el navegador, no solo al compilar.** Una variable de Sass desaparece cuando se
   genera el CSS. Una custom property sigue viva: podés verla y cambiarla en las DevTools, y
   podés leerla desde JavaScript. Por eso no necesitás ningún paso de build.
2. **Se heredan y se pueden redefinir por contexto.** Si declarás `--color-fondo` en `:root` y
   la redeclarás dentro de `.panel-oscuro`, todo lo que esté dentro de ese panel usa el valor
   nuevo sin tocar una sola regla más. Es el mecanismo con el que se hace un modo oscuro en
   diez líneas.
3. **`:root` es simplemente el elemento `<html>`.** Se usa ese selector por convención porque
   es el ancestro de todo, así que lo que declares ahí lo hereda la página entera.

Y el detalle que importa para vos: cuando alguien abre tu proyecto y ve un archivo con treinta
custom properties bien nombradas, lee "esta persona diseñó un sistema". Cuando ve `#2563eb`
repetido en catorce sitios, lee lo contrario.

- [ok ] Leer la guía de MDN sobre custom properties:
  https://developer.mozilla.org/es/docs/Web/CSS/Using_CSS_custom_properties
- [ok ] Abrir **Open Props** y navegar la documentación: https://open-props.style/
- [ok ] Mirar en concreto tres secciones suyas: **Sizes** (escala de espaciado), **Typography**
  (escala tipográfica) y **Shadows** (sombras)
- [ok ] Anotar tres cosas de su criterio que quieras imitar y una que no

->> MIS NOTAS:

- a tener en cuenta: valores definidos para los border-round con xs, sm, md, lg, xl. Colores tipo primary, secondary, danger, warning, success, y despues para textos y fondos mas un accent. No usar white ni black al 100% sino al 4% y 85% respectivamente.
- A imitar:
  1. static-sizes (con px, no rem), con menos opciones (mas acotado, algunas son muy similares por ejemplo: 16-20-24)
  2. font-sizes, font-weight
  3. shadows. solo box-shadow
- No imitar:
  1. No todos los valores. Solo los que necesite en el diseño.

- [ ok] Abrir las DevTools en cualquier sitio que ya use variables y cambiar una en vivo, para
  ver cómo se propaga

- **Ojo con Open Props:** **no lo instales.** No es una dependencia de este proyecto, es una
  referencia. La idea es mirar cómo alguien que sabe construye una escala — cuántos pasos
  tiene, cómo los nombra, dónde corta — y después construir la tuya. Copiás el criterio, no el
  archivo. Si lo instalás, volvés a estar usando el sistema de diseño de otro, que es
  exactamente lo que decidimos no hacer.
- **Hecho cuando:** podés explicar en una frase por qué una custom property no es lo mismo que
  una variable de Sass, y tenés anotado qué te llevás de Open Props.

### C3. Bocetar en Figma

- **Objetivo:** tener decidido cómo se ve la app **antes** de escribir CSS.
- **Por qué:** improvisar el diseño mientras peleás con el CSS es hacer dos cosas difíciles a
  la vez, y las dos salen mal. Además, para un portfolio de diseño el proceso vale tanto como
  el resultado: los bocetos son material que vas a querer mostrar.

- [ ok] Crear el archivo de Figma con dos frames de ancho fijo: **360 px** y **1440 px**
- [ ok] **Empezar por el de 360 px.** Sí, primero el móvil, aunque duela
- [ ] Bocetar los cuatro patrones, no las diecisiete pantallas:
  - [ ] **El esqueleto** — cabecera, navegación, contenido (equivale a `base.html` + D2)
  - [ ] **Un listado** — tabla con buscador y paginación (`l_empresa`, el más simple del grupo)
  - [ ] **Un formulario** — `altas.html`, que es el genérico que usan casi todas las altas
  - [ ] **Un detalle** — `v_empresa`, pares etiqueta/valor
- [ ] Repetir los cuatro en el frame de 1440 px
- [ ] Definir en Figma los **estilos** (colores y tipografías como estilos reutilizables, no
      valores sueltos): son el borrador de tus tokens de C4
- [ ] Bocetar los tres **estados que siempre se olvidan**: qué se ve cuando una tabla está
      vacía, cuando la búsqueda no encuentra nada, y cómo se ve un campo con error
- [ ] Exportar los bocetos a `docs/bocetos/` y commitearlos

- **Por qué empezar por 360 px:** es más difícil, y es lo que fuerza las decisiones reales.
  ¿Cuáles de las 9 columnas de `l_cli_pro` sobreviven en un móvil? ¿Dónde va la navegación con
  6 secciones? Si resolvés eso, lo de escritorio sale casi solo. Al revés, hacés un Figma
  bonito de escritorio y descubrís en el navegador que en móvil no cierra.
- **Por qué no bocetar las 17:** porque con esos cuatro patrones el resto son variaciones.
  Bocetar quince pantallas antes de tocar código es cómo se muere un rediseño.
- **Trampa:** en Figma podés poner cualquier tamaño de texto y cualquier color, y todo se ve
  bien. Antes de dar un boceto por bueno, comprobá que los tamaños salen de una escala y que
  los contrastes pasan (hay plugins de contraste para Figma, pero el criterio es el mismo que
  en C4).
- **Hecho cuando:** podés mirar los bocetos y saber exactamente qué CSS tenés que escribir, sin
  ninguna decisión visual pendiente.

### C4. Definir los tokens de diseño

- **Objetivo:** un archivo CSS con tus variables base, antes de escribir ningún componente.
- **Por qué:** los _tokens_ son el vocabulario: colores, escala tipográfica, escala de espaciado,
  radios, sombras. Si están centralizados, cambiar la identidad de toda la app es editar diez
  líneas. Es lo que separa "CSS" de "sistema de diseño", y es justo lo que un portfolio de
  diseño quiere ver.

- [ ] Crear `static/css/tokens.css` (nuevo, no toques todavía los que ya están)
- [ ] Definir la **escala de espaciado**
- [ ] Definir la **escala tipográfica** y elegir familia(s)
- [ ] Definir los **colores por rol**
- [ ] Definir radios y sombras
- [ ] Comprobar el contraste de **cada** par texto/fondo
- [ ] Enlazar `tokens.css` en `base.html` y comprobar que carga (aunque todavía no se note nada)

- **Pistas:** las **custom properties** que viste en C2 son el mecanismo. Sobre las decisiones:
  - **Espaciado:** elegí una escala, no valores al azar. Una progresión basada en 4px u 8px
    (4, 8, 12, 16, 24, 32, 48…) cubre casi todo. La regla real es: si escribís un `16px` suelto
    en un componente, es que te falta un token.
  - **Tipografía:** una escala modular (cada tamaño es el anterior por un factor constante)
    da jerarquía coherente. Dos familias como máximo, y una sola ya es una decisión válida.
  - **Color:** definí roles, no nombres de color. `--color-superficie` y `--color-peligro` sobreviven
    a un rediseño; `--azul-claro` no. Vas a necesitar al menos: fondo, superficie elevada, texto
    principal, texto secundario, borde, acento, y los estados de éxito/error/aviso.
  - **Contraste:** cada par texto/fondo tiene que llegar a **4.5:1** (WCAG AA) para texto normal
    y 3:1 para texto grande. Comprobalo _mientras_ elegís, no después: reelegir la paleta entera
    porque el gris claro no contrasta duele mucho más tarde. Hay verificadores online y las
    DevTools te lo muestran en el selector de color.
- **Trampa clásica:** no empieces por "quiero que sea azul". Empezá por cuántos niveles de
  jerarquía necesitás. El color viene después.
- **Hecho cuando:** tenés un archivo de tokens y podés cambiar el acento de la app entera
  editando una línea.

### C5. Decidir la estrategia de layout

- **Objetivo:** saber, antes de maquetar, cómo se comporta la app en móvil, tablet y escritorio.
- **Por qué:** hoy la estructura es una barra superior fija más un `aside` lateral, heredada de
  una plantilla de Bootstrap 3. En móvil, eso no funciona (y de hecho hoy está roto, ver D2).

- [ ] Anotar tus **breakpoints**, mirando dónde se rompe tu contenido
- [ ] Decidir la estructura de página (Grid) y escribirla en los bocetos de C3
- [ ] Decidir qué pasa con la navegación en móvil (ver la decisión de diseño de D2)
- [ ] Dibujar en papel las tres versiones del layout

- **Pistas:**
  - **Mobile-first**: escribí primero el CSS del móvil y usá `min-width` en los media queries para
    ir añadiendo. Al revés se sufre mucho más.
  - Los _breakpoints_ se eligen mirando **dónde se rompe tu contenido**, no copiando los de Bootstrap.
    Ensanchá el navegador despacio y anotá en qué anchos algo se ve mal: ahí van.
  - Investigá `clamp()` para tipografía y espaciados fluidos: reduce la cantidad de media queries
    que necesitás.
  - Grid para la estructura de página, Flexbox para agrupar elementos en una línea. Si dudás:
    Grid es bidimensional, Flexbox unidimensional.
- **Hecho cuando:** podés dibujar en papel las tres versiones del layout antes de escribir CSS.

### C6. Escribir la base CSS propia

- **Objetivo:** los cimientos de tu CSS, sobre los que la Fase D va a construir pantalla por
  pantalla.
- **Por qué:** son las reglas que valen para toda la app y que no pertenecen a ninguna pantalla
  en particular. Si no las escribís ahora, las vas a ir improvisando quince veces en la Fase D.

- [ ] Crear `static/css/base.css` con un **reset moderno**
- [ ] Definir los estilos base de los elementos HTML: `body`, títulos, párrafos, enlaces,
      listas, `table`
- [ ] Definir un **`:focus-visible` global y bien visible** (esto es obligatorio, ver abajo)
- [ ] Definir el estilo del **skip link** de D1
- [ ] Crear `static/css/componentes.css` (vacío por ahora; lo va llenando la Fase D)
- [ ] Enlazar los tres archivos en `base.html` en el orden correcto: tokens → base → componentes
- [ ] Comprobar en el navegador que el conjunto carga y que Bootstrap sigue mandando
      (todavía es así, y está bien)

- **Pistas:**
  - **El reset:** no copies el `reset.css` de Meyer de 2007, que borra absolutamente todo.
    Buscá "modern CSS reset" (el de Andy Bell es el de referencia): son unas 30 líneas que
    arreglan lo que molesta —`box-sizing: border-box`, márgenes por defecto, imágenes que se
    desbordan— y **conservan** lo que el navegador ya hace bien.
  - **Sobre `:focus-visible`:** nunca escribas `outline: none` sin poner un reemplazo. Quien
    navega con teclado deja de saber dónde está. Es el error de accesibilidad más frecuente y
    más fácil de evitar del mundo del CSS.
  - **Sobre el orden de los archivos:** en CSS, a igual especificidad gana el último que se
    declara. Tokens primero (solo declara variables, no pinta nada), base después, componentes
    al final.
  - **Regla para saber si algo va en `base.css` o en `componentes.css`:** si estás estilando un
    elemento HTML (`h1`, `table`, `a`), va en base. Si estás estilando una clase tuya
    (`.tarjeta`, `.boton`), va en componentes.
- **Hecho cuando:** podés recorrer cualquier pantalla con Tab y siempre ves dónde está el foco,
  y los tres archivos cargan en orden.

### C7. Corregir el `<head>` de `base.html`

- **Objetivo:** el documento base es correcto y accesible.
- **Por qué:** hay tres problemas concretos ahí, y son la base de todo lo demás:
  1. **`<html >` no tiene atributo `lang`.** Los lectores de pantalla lo usan para saber en qué
     idioma pronunciar. Sin él, un texto en español puede leerse con fonética inglesa. Es un
     fallo de WCAG de nivel A, el más básico.
  2. **El viewport bloquea el zoom:** `user-scalable=no, maximum-scale=1.0`. Eso impide a una
     persona con baja visión ampliar la página en el móvil. Incumple WCAG 1.4.4. Era una
     costumbre común en 2017 y hoy se considera un error claro.
  3. **El `<title>` está fijo** en "Gestion de IVA" para todas las páginas. El título es lo primero
     que anuncia un lector de pantalla y lo que se ve en la pestaña y en favoritos.

- [ ] Añadir `lang="es"` al `<html>`
- [ ] Arreglar el viewport: fuera `user-scalable=no` y `maximum-scale`
- [ ] Convertir el `<title>` en un bloque que cada plantilla hija rellena
- [ ] Cambiar las rutas `/static/css/...` escritas a mano por `{% static %}`
- [ ] **Hacer lo mismo en `login_form.html` y `logout_form.html`**, que tienen su propio
      `<head>` con los mismos tres fallos — o mejor, pasarlas a heredar de `base.html`
- [ ] Pasar la página por un validador de HTML

- **Pistas:** para el título, investigá cómo se define un bloque en la plantilla base que cada
  hija pueda rellenar (ya usás `{% block content %}`, es el mismo mecanismo). Fijate que tus vistas
  ya pasan una variable `title` en el contexto: aprovechala.
- **Extra:** las rutas a los CSS están escritas a mano como `/static/css/...`. Django tiene una
  etiqueta para esto (`{% static %}`, y `base.html` ya carga la librería en la primera línea).
  Buscá por qué importa: pista, tiene que ver con poder mover los archivos o servirlos desde otro
  dominio sin editar plantillas.
- **Bonus:** al pasar `login_form.html` a `{% static %}` se arregla solo el 404 de
  `bootstrap.css` que encontraste en C1 — o al menos vas a ver el error claramente en vez de
  en silencio.
- **Hecho cuando:** validás la página en un validador de HTML sin errores, podés hacer zoom en el
  móvil, y cada pantalla muestra su propio título en la pestaña.

### C8. Sacar `crispy_forms`

- **Objetivo:** ningún formulario del proyecto pasa por crispy. El HTML de los campos lo
  escribís vos, en una plantilla, una sola vez.
- **Por qué:** el razonamiento completo está en `NOTAS_FASE_C.md`, sección 2. El resumen:
  crispy **no** obliga a usar Bootstrap (trae un pack `uni_form` que no lo usa), pero
  **ninguno de sus packs emite un solo atributo ARIA** — comprobado. Sin `aria-describedby`
  ni `aria-invalid` no podés cumplir lo que piden D3 y D6. Y hay algo peor: hoy tu grilla
  responsive está escrita en Python (`self.helper.label_class = "col-lg-3 col-sm-3"`), que es
  justo el acoplamiento que esta fase existe para romper.
- **De regalo:** sacarlo elimina un renglón de la Fase F. Crispy 2.x separó los template packs
  a paquetes aparte y esa migración está rota; si no usás crispy, no te afecta.

**Hacelo en este orden. Cada paso deja la app funcionando.**

- [ ] **1. Guardar el "antes".** Abrí `/a_empresa/` en el navegador, "ver código fuente", y
      guardá el HTML que genera crispy hoy en un archivo aparte. Es tu referencia de qué
      estás reemplazando — y de qué no querés reemplazar
- [ ] **2. Escribir `templates/includes/campo.html`**, el partial que renderiza **un** campo:
      su `<label>`, el widget, el texto de ayuda y sus errores, con los `aria-*` bien puestos.
      Es el archivo más importante de toda la fase: lo van a usar los cinco formularios
- [ ] **3. Migrar `login_form.html`** (línea 29, `{{ form|crispy }}`). Es la más chica:
      dos campos. Empezá acá para validar que `campo.html` funciona
- [ ] **4. Comprobar el login a mano** en el navegador, con credenciales buenas y malas.
      Los errores tienen que verse y estar asociados al campo
- [ ] **5. Migrar `altas.html`** (línea 8, `{% crispy form form.helper %}`). Ojo: esta
      plantilla la usan las altas de empresa, de cliente/proveedor, de libro **y el registro
      de usuarios**. Probá las cuatro
- [ ] **6. Limpiar `IVAcompras/forms.py`:** borrar los `FormHelper`, los `Layout`, los
      `label_class`/`field_class` y los `add_input(Submit(...))` de `CliProForm`,
      `EmpresaForm` y `LibroForm`. Los `Meta` y los `fields` **se quedan**
- [ ] **7. El caso difícil: `DetalleForm`.** 17 campos, dos columnas, un `<fieldset>`
      "Valores" y diez `PrependedText` con el "$". Ese layout pasa de Python a HTML
- [ ] **8. Limpiar `cuentas/forms.py`:** el `FormHelper` de `UserRegisterForm` (líneas 58-70)
      y los imports de crispy (líneas 3-4). `UserLoginForm` no tiene helper, no la toques
- [ ] **9. Borrar los `{% load crispy_forms_tags %}`** de las tres plantillas. Fijate que
      `logout_form.html:2` lo carga y **nunca usa crispy**: eso ya era código muerto
- [ ] **10. Sacar la dependencia:** `"crispy_forms"` y `CRISPY_TEMPLATE_PACK` de
      `IVA/settings.py` (líneas 65 y 72), y `django-crispy-forms==1.11.0` de `requirements.txt`
- [ ] **11. Desinstalar:** `pip uninstall django-crispy-forms`
- [ ] **12. `python manage.py test`** — los 9 tests en verde
- [ ] **13. Recorrer las cinco pantallas de formulario a mano** y comprobar que se puede
      enviar cada una

- **Pistas para `campo.html`:**
  - Un formulario de Django se puede recorrer con `{% for field in form %}`, y cada `field`
    tiene `label`, `id_for_label`, `errors`, `help_text` y `field.required`. Con eso tenés
    todo lo que necesitás
  - Para asociar los errores y la ayuda al campo, el atributo es `aria-describedby` en el
    input, apuntando al `id` del elemento que los contiene. Los `id` los podés construir a
    partir de `field.auto_id`
  - No te olvides de `{{ form.non_field_errors }}`: son los errores del formulario entero, no
    de un campo. `UserLoginForm` los usa (todos sus `ValidationError` del `clean()` caen ahí)
  - Los campos ocultos (`libro` en `DetalleForm`) se pintan sueltos, sin label ni envoltorio.
    Django te lo dice con `field.is_hidden`
- **Trampa:** el `{% csrf_token %}` no lo pone crispy en `login_form.html` (mirá la línea 28,
  está a mano) pero **sí** lo pone el `{% crispy %}` de `altas.html`, que genera el `<form>`
  entero. Al sacar crispy de ahí, el `<form>`, el `method="POST"`, el `{% csrf_token %}` y el
  botón de enviar los tenés que escribir vos. Si te olvidás del token, Django te va a devolver
  un 403 al enviar — y ahora ya sabés por qué.
- **Ojo con los widgets:** Django sigue generando el `<input>` por su cuenta con `{{ field }}`,
  pero **sin ninguna clase CSS**. El `class="form-control"` que ves hoy en el HTML lo ponía
  crispy, no Django: cuando saques crispy, desaparece. Si querés clases propias en los inputs,
  se declaran con `Meta.widgets` en el formulario. Pero antes de hacerlo, pensá si de verdad
  las necesitás: con `input[type="text"]`, `select` o `textarea` como selectores en tu CSS
  llegás al mismo sitio sin volver a meter presentación dentro de Python.
- **Hecho cuando:** `grep -rn "crispy" templates/ IVAcompras/ cuentas/ IVA/` no devuelve nada,
  los 9 tests pasan, y enviaste con éxito los cinco formularios a mano.

### C9. Sacar las dependencias muertas

- **Objetivo:** que el proyecto no cargue ni instale nada que no use.
- **Por qué:** cada una de estas es peso muerto que alguien va a tener que entender algún día.
  Y las tres se pueden quitar **sin que cambie nada visualmente**, que es lo que las hace
  candidatas de la Fase C y no de la D.

- [ ] **`django-bootstrap3`** — está en `INSTALLED_APPS` (`settings.py:67`) y **ninguna
      plantilla la carga**: cero `{% load bootstrap3 %}`, cero `{% bootstrap_form %}`.
      Verificalo vos con grep antes de borrar, y después sacala de `settings.py`, de
      `requirements.txt` y del entorno con `pip uninstall`
- [ ] **El jQuery duplicado** — `base.html:36-37` carga `jquery.js` **y** `jquery-1.12.4.js`.
      Dejá uno solo
- [ ] **Los datepickers de jQuery UI** — reemplazá los cuatro (`altas.html:36`,
      `i_libro.html:45-46`, `i_dgr.html` y `v_libro.html:133-134`) por `<input type="date">`
      nativo. Es accesible, funciona en móvil y no necesita ninguna librería
- [ ] **jQuery UI entero** — una vez fuera los datepickers, comprobá que nadie más lo usa y
      borrá `jquery-ui.js` y `jquery-ui.css` (36 KB de CSS) del `<head>` de las tres
      plantillas que los enlazan
- [ ] **El modal muerto de `altas.html`** (líneas 15-29 más el JS de la 41): `#acpmodal` con
      el cuerpo vacío y un handler para `#btnguardar`, que no existe. Restos de
      `a_cp_modal.html`, borrada en B4
- [ ] **`IVAcompras/urls.py:2`** — `from django.contrib import admin` sin usar. Es el único
      aviso real de pyflakes en todo el proyecto
- [ ] Correr los tests y recorrer las pantallas que tocaste

- **Ojo con `<input type="date">`:** el formato que envía el navegador es `AAAA-MM-DD`, que no
  tiene por qué ser el que espera tu formulario hoy. Mirá `DATE_INPUT_FORMATS` en la
  documentación de Django 1.11 y comprobá que el POST sigue guardando bien la fecha. Es el
  único punto de este paso donde algo puede romperse en silencio: probalo, no lo asumas.
- **Ojo con `i_libro` e `i_dgr`:** ahí los campos no son fechas completas sino mes y año
  sueltos (`?m=...&a=...`). `type="date"` no sirve; mirá `type="month"`, o un `<select>` para
  el mes y un `type="number"` para el año. Decidilo vos, pero el `<input type="text">` con
  datepicker de jQuery se va igual.
- **Lo que NO se borra todavía:** `bootstrap_modif.css`, `bootstrap.js`, `font-awesome.css` e
  `iva.css`/`iva2.css`. Las plantillas todavía dependen de ellas. Eso es D8.
- **Hecho cuando:** los 9 tests pasan, `pip list` no tiene crispy ni bootstrap3, y la app se
  ve **exactamente igual** que antes de esta tarea. Si se ve distinta, borraste algo de más.

### C10. Cierre de la fase

- [ ] Los 9 tests en verde
- [ ] Recorrer las 17 pantallas a mano: ninguna reventó
- [ ] `pip list` y `requirements.txt` coinciden
- [ ] Los tokens documentados: un comentario arriba de `tokens.css` explicando la escala que
      elegiste y por qué
- [ ] Commits chicos y con mensaje descriptivo (uno por tarea, mínimo)
- [ ] Mergear `refactor-redesign` a `master`

- **Hecho cuando:** tenés los cimientos puestos —tokens, base, bocetos, formularios propios—
  y la app se ve igual que al empezar la fase. Eso último no es un fracaso: es exactamente lo
  que buscábamos. **La Fase C no cambia cómo se ve la app; construye las herramientas con las
  que la Fase D la va a cambiar.**

---

## FASE D — Rediseño vista por vista

Diecisiete plantillas (quince en `templates/` más dos en `templates/includes/`; eran diecinueve
antes de la limpieza de B4). **No las ataques en orden alfabético**: seguí el orden de abajo, que va de
lo estructural a lo específico. Cada grupo comparte patrones, así que al terminar el primero de
cada grupo los demás salen rápido.

Antes de empezar: creá tu rama, y **sacá capturas del estado actual**. Las vas a querer para el
"antes y después" del portfolio, y una vez que rediseñes ya no hay vuelta atrás.

### D1. `base.html` — el esqueleto

Todo lo demás hereda de acá, así que va primero.

- **Objetivo:** estructura semántica, tokens aplicados, layout responsive funcionando.
- **Tips de accesibilidad:**
  - Usá landmarks reales: `<header>`, `<nav>`, `<main>`, `<footer>`. Hoy hay `<header>` y `<aside>`,
    pero **el contenido principal está en un `<div class="container">**: debería ser `<main>`.
    Los lectores de pantalla permiten saltar directamente al `<main>`.
  - Añadí un **skip link** ("Saltar al contenido") como primer elemento enfocable. Para quien navega
    con teclado, evita tabular por todo el menú en cada página. Se oculta visualmente hasta que
    recibe foco: buscá el patrón, es un clásico y tiene truco (no sirve `display: none`).
  - Definí un estilo de `:focus-visible` global y visible. **Nunca** `outline: none` sin reemplazo:
    quien navega con teclado deja de saber dónde está.
- **Hecho cuando:** podés recorrer la página entera con Tab viendo siempre dónde estás.

### D2. `includes/menu.html` y `includes/aside.html` — la navegación

Es lo que más se usa de toda la app, y hoy tiene dos fallos serios.

- **Bug confirmado #1:** el botón hamburguesa dice `data-toggle="collpase"` — **está mal escrito**
  ("collpase" en vez de "collapse"). Además apunta a `#bs-example-navbar-collapse-1`, un div que
  está comentado más abajo. Traducción: **el menú móvil no funciona hoy**. Compruébalo achicando
  la ventana antes de rediseñar; entender el bug antes de borrarlo es parte del ejercicio.
- **Bug confirmado #2:** los submenús del `aside` son `<a href="javascript:void(0);">`. Un enlace
  que no lleva a ningún sitio pero abre/cierra algo **es un botón, no un enlace**. Hoy no se puede
  usar con teclado y un lector de pantalla lo anuncia como enlace.
- **Tips:**
  - Elemento interactivo que no navega → `<button>`. Que navega → `<a href>`. Esta única regla
    resuelve el 80% de los problemas de accesibilidad en menús.
  - Para desplegables, investigá `aria-expanded` y `aria-controls`: comunican al lector de pantalla
    si está abierto y qué controla. Tienen que **actualizarse con JS** al abrir/cerrar, no ser fijos.
  - Marcá la sección activa con `aria-current="page"`, y que se note también visualmente.
  - Verificá que el menú se puede abrir, recorrer y cerrar (con `Escape`) sin tocar el ratón.
  - Área táctil mínima recomendada: 44×44px. Medila en las DevTools, no a ojo.
- **Decisión de diseño:** ¿mantenés el patrón barra superior + lateral, o unificás? Con seis
  secciones, un lateral fijo puede ser mucho peso visual. Pensalo en móvil primero.

### D3. `login_form.html` y `logout_form.html` — entrada

Pantallas chicas, ideales para estrenar tus tokens y ver el sistema funcionando.

- **Tips:**
  - Todo campo necesita un `<label>` asociado (`for` ↔ `id`). Un `placeholder` **no es una etiqueta**:
    desaparece al escribir y muchos lectores de pantalla lo ignoran.
  - Usá `autocomplete="username"` y `autocomplete="current-password"`: los gestores de contraseñas
    los necesitan para rellenar bien.
  - Los errores tienen que ser perceptibles sin depender del color (un color rojo no lo ve
    todo el mundo): sumá icono y texto. Asocialos al campo con `aria-describedby`.
  - Si el formulario falla entero, un resumen de errores al principio, enfocable, ahorra mucho.
- **Nota:** esta duda ya está resuelta. Cuando escribimos este plan, estos formularios usaban
  `crispy_forms` y la pregunta era si escribirlos a mano o hacerle un _template pack_ propio.
  **Se decidió sacar crispy** (tarea C8, razonamiento en `NOTAS_FASE_C.md`), así que al llegar
  acá el HTML de los campos ya es tuyo: vive en `templates/includes/campo.html`. Lo que te toca
  en D3 es **diseñarlo**, no decidir de dónde sale.

### D4. `home.html` — el panel principal

- **Contexto:** muestra una tabla de empresas con sus libros de ventas y compras, marcando con
  "X" los que no existen.
- **Tips:**
  - Es la primera pantalla tras el login: tiene que responder "¿qué hago acá?" en dos segundos.
  - Ese "X" que marca ausencia es información importante comunicada solo por una letra suelta.
    Pensá cómo se entiende sin contexto, y qué escucha alguien con lector de pantalla.
  - Si es la pantalla de trabajo diaria, las acciones frecuentes deberían estar a un clic.
    Mirá qué hace hoy el usuario para llegar a lo que más usa y contá los clics.

### D5. Listados: `l_empresa.html`, `l_cli_pro.html`, `l_libro.html`, `usuarios.html`

Cuatro plantillas con el mismo patrón (tabla + buscador + paginación). Resolvé una bien y replicá.
**Es el grupo con más impacto visual del proyecto.**

- **Tips de tablas:**
  - Mantené `<table>`: son datos tabulares de verdad, y ese es su elemento. No las conviertas
    en `<div>`. El error opuesto también existe: no uses tablas para maquetar.
  - Añadí `<caption>` (podés ocultarlo visualmente) y `scope="col"` en cada `<th>`. Sin `scope`,
    un lector de pantalla no puede relacionar cada celda con su cabecera. Hoy no lo tiene ninguna.
  - Quitá `align="center"` de `l_empresa.html:18`: es HTML presentacional de los años 90, eso es CSS.
  - **Responsive de tablas:** el scroll horizontal es la salida fácil pero mediocre. Investigá el
    patrón de "tarjetas en móvil" (cada fila se convierte en una tarjeta con etiqueta+valor).
    Requiere pensar qué columnas son imprescindibles en pantalla chica: de las 9 de
    `l_cli_pro.html`, ¿cuántas necesita alguien en el móvil?
  - Ojo con `truncatechars`: hoy corta a 15-25 caracteres. Si el ancho lo maneja el CSS, quizá
    ya no haga falta cortar el dato en la plantilla.
  - Pensá el **estado vacío**: ¿qué se ve cuando no hay ninguna empresa todavía, o cuando la
    búsqueda no encuentra nada? Hoy se ve una tabla vacía sin explicación. Es de los detalles
    que más distinguen a un diseño cuidado.
- **Tips del buscador:** el campo de `l_empresa.html:9` tiene `placeholder` pero **ningún `<label>`**.
  Mismo problema en los otros listados. Investigá cómo etiquetar un buscador sin que la etiqueta
  se vea (hay técnicas correctas y hay `display:none`, que es la incorrecta: piensa por qué).
- **Tips de paginación:** debe ir dentro de un `<nav>` con `aria-label`, indicar la página actual
  con `aria-current`, y los enlaces necesitan texto comprensible fuera de contexto ("Página 3",
  no "3" a secas, aunque visualmente se vea solo el número).

### D6. Formularios: `altas.html`, `importar.html`, `i_libro.html`, `i_dgr.html`

`altas.html` es genérico: lo usan las altas de empresa, cliente/proveedor **y el registro de
usuarios**. Cambiarlo afecta a varias pantallas: verificalas todas.

- **Tips:**
  - Una sola columna. Los formularios de dos columnas confunden el orden de lectura y complican
    el orden de tabulación.
  - Agrupá campos relacionados con `<fieldset>` y `<legend>`.
  - Marcá los obligatorios de forma redundante: asterisco **y** texto, no solo color.
  - `inputmode` y `type` correctos: un CUIT o un teléfono en el móvil deberían abrir teclado
    numérico. Detalle chico, gran diferencia de uso.
  - Los mensajes de error, junto al campo, no todos amontonados arriba (o los dos, pero nunca
    solo arriba).
  - En `importar.html` hay una subida de archivo: los `<input type="file">` nativos son feos pero
    accesibles. Si lo estilás, cuidá no romper el foco por teclado ni el nombre del archivo elegido.
    Y pensá el feedback: ¿qué ve el usuario mientras se procesa un Excel grande?

### D7. Detalles: `v_empresa.html`, `v_cli_pro.html`, `v_libro.html`, `v_detalle.html`

- **Tips:**
  - Son pares etiqueta/valor: `<dl>`, `<dt>` y `<dd>` existen exactamente para eso y casi nadie
    los usa. Buen detalle semántico para mostrar en un portfolio.
  - Jerarquía clara: lo identificatorio arriba y grande, lo secundario después.
  - Las acciones (editar, borrar, exportar) siempre en el mismo sitio en las cuatro pantallas.
  - **El borrado necesita confirmación.** Confirmado en `d_empresa` (`views.py:277`): visitar la
    URL borra el registro y redirige, sin preguntar nada. Revisá `d_cli_pro`, `d_libro` y
    `d_detalle`, que siguen el mismo patrón. Es un problema de diseño _y_ de seguridad: un borrado
    nunca debería ocurrir con un GET (basta con que un navegador precargue el enlace). Investigá
    por qué, buscando "métodos seguros e idempotentes" en HTTP. Es tema de la Fase B tanto como
    de esta.
  - `v_libro.html` tiene una tabla de 10 columnas: es la más difícil de hacer responsive de todo
    el proyecto. Dejala para el final del grupo, cuando ya tengas el patrón resuelto en D5.

### D8. Revisión final del rediseño

- [ ] Recorrer las 19 pantallas con el teclado, sin ratón
- [ ] Verlas todas a 360px de ancho y a 1920px
- [ ] Pasar un auditor automático (Lighthouse en las DevTools, o axe DevTools) por cada una
- [ ] Comprobar el contraste real con las DevTools, no de memoria
- [ ] Probar con zoom del navegador al 200%: WCAG lo exige y rompe muchos diseños fijos
- [ ] Borrar el CSS viejo que ya no se usa (`bootstrap_modif.css`, `jquery-ui.css`, `iva2.css`…)
      y comprobar que no se rompe nada
- [ ] Sacar las capturas del "después"

---

## FASE E — Portfolio

Con el código limpio y el diseño nuevo, esto es lo que convierte el trabajo en una pieza.

- [ ] **Reescribir el `README.md`**: qué problema resuelve la app y para quién, capturas del
      resultado, stack, y una sección de decisiones técnicas. Hoy el README tiene notas de tareas
      de 2017 que ya no aplican y una sección de instalación desactualizada: borralas.
- [ ] **Contar el "antes y después"** con las capturas. Demuestra criterio, que vale más que el
      resultado en sí.
- [ ] **Escribir qué aprendiste** en el proceso. Un párrafo honesto sobre qué estaba mal y por qué
      lo cambiaste vale más que cualquier lista de tecnologías.
- [ ] Revisar que el historial de commits reciente se pueda leer sin vergüenza.

---

## FASE F — Migración a Django 5.x

**Al final, y como proyecto aparte.** Hoy estás en 1.11 (sin soporte desde 2020). No hace falta
para que la app funcione, pero es el ejercicio de Python más valioso que este proyecto puede darte,
y quita del portfolio la señal de "stack de 2017".

**No empieces esta fase sin los tests de B6.** Sin ellos, migrar es adivinar.

Superficie de cambio ya medida:

| Qué rompe                                      | Dónde                               | Cuánto                   |
| ---------------------------------------------- | ----------------------------------- | ------------------------ |
| `url()` con regex → `path()` / `re_path()`     | `IVA/urls.py`, `IVAcompras/urls.py` | 39 rutas                 |
| `include(namespace=)` sin `app_name`           | `IVA/urls.py:19`                    | 1 (bloquea el arranque)  |
| `user.is_authenticated()` como método          | vistas                              | 32 → **0 si hiciste B1** |
| `ForeignKey` sin `on_delete`                   | `models.py:48,65,77`                | 3                        |
| `{% load staticfiles %}` → `{% load static %}` | `base.html:1`                       | 1                        |
| `ugettext_lazy` → `gettext_lazy`               | `settings.py:127`                   | 1                        |

Fijate en la tercera fila: **la Fase B te ahorra el 40% de esta migración**. Por eso va antes.

- [ ] Leer las notas de versión de cada salto (1.11→2.0→2.2→3.0→3.2→4.0→4.2→5.x). Sí, todas:
      las secciones de "backwards incompatible changes" son cortas y son el mapa
- [ ] Decidir la estrategia: salto directo a 5.x, o escalonado versión por versión. El escalonado
      es más lento pero cada paso te avisa de sus propias deprecaciones. En producción real se hace así
- [ ] Actualizar también Python: 3.8 está sin soporte desde octubre de 2024. Django 5.x pide 3.10+
- [ ] Revisar las dependencias: `django-import-export 0.6.0` es de la misma época y necesita
      salto. **`django-crispy-forms` ya no está** — lo sacaste en C8, y con él se fue la
      migración más fea de esta lista (crispy 2.x separó los template packs a paquetes aparte).
      Lo mismo con `django-bootstrap3`, eliminada en C9. Dos renglones menos, gratis
- [ ] Ejecutar con `-W error::DeprecationWarning` para que los avisos salten como errores
- [ ] Los tests de B6 en verde al terminar

---

## Anexo: hallazgos ya detectados

Inventario de lo que encontré revisando el proyecto, para que no tengas que buscarlo. Cada uno
está referenciado en la tarea que le corresponde.

**Repositorio y configuración**

- Hashes de contraseña reales publicados en GitHub (PBKDF2, 30.000/36.000 iteraciones) → A1
- `db.sqlite3` versionado: ruido en cada `git status` y datos personales en el repo → A3, A5
- `SECRET_KEY` en texto plano en `IVA/settings.py:22` → A6
- `DEBUG = True` fijo en `settings.py:26` → A6
- `static_root/` versionado (son archivos generados por `collectstatic`) → A5
- No hay forma documentada de que un tercero levante el proyecto con datos → A7

**Código**

- 32 chequeos de login copiados a mano → B1
- 16 `print()` de depuración → B2
- `IVAcompras/views.py`: 745 líneas, 28 funciones → B7
- `from .models import *` y `from .forms import *` → B5
- `tests.py` vacíos en las dos apps → B6
- `/l_detalle/` revienta: falta `l_detalle.html` (verificado) → B3
- `pruebas.html` y `a_cp_modal.html` huérfanos → B4
- Los borrados parecen ejecutarse por GET sin confirmación → D7 (verificalo)

**HTML y accesibilidad**

- `<html >` sin atributo `lang` → C7
- Viewport bloquea el zoom (`user-scalable=no`) → C7
- `<title>` fijo para todas las páginas → C7
- Rutas `/static/` a mano en vez de `{% static %}` → C7
- `login_form.html` y `logout_form.html` no heredan de `base.html`: `<head>` duplicado
  por triplicado, con los mismos tres fallos de arriba → C1, C7
- Menú móvil roto: `data-toggle="collpase"` (typo) apuntando a un div comentado → D2
- Submenús con `href="javascript:void(0)"` en vez de `<button>` → D2
- Ninguna tabla tiene `<caption>` ni `scope` en sus `<th>` → D5
- Buscadores sin `<label>` en los listados → D5
- `align="center"` en `l_empresa.html:18` → D5
- El contenido principal es un `<div>`, no un `<main>` → D1

**CSS**

- `bootstrap_modif.css`: 6.761 líneas, uso real por verificar → C1
- **`login_form.html` y `logout_form.html` enlazan `/static/css/bootstrap.css`, que NO existe
  en `static/` (solo en `static_root/`, que sacaste del repo en A5). Verificado: da 404.
  La pantalla de login se ve sin estilos en cualquier clon nuevo** → C1, C7
- Dependencias de otra época: Bootstrap 3, jQuery UI, Font Awesome 4 → C1
- jQuery cargado dos veces en `base.html:36-37` (`jquery.js` y `jquery-1.12.4.js`) → C9
- Datepickers de jQuery UI en 4 plantillas, reemplazables por `<input type="date">` nativo → C9

**Dependencias y código muerto**

- `django-bootstrap3` en `INSTALLED_APPS` sin que ninguna plantilla la cargue → C9
- Modal `#acpmodal` huérfano en `altas.html:15-29` + handler para `#btnguardar`, que no
  existe (restos de `a_cp_modal.html`, borrada en B4) → C9
- `{% load crispy_forms_tags %}` en `logout_form.html:2` sin usar crispy en ningún lado → C8
- `from django.contrib import admin` sin usar en `IVAcompras/urls.py:2` → C9
- Ningún template pack de crispy 1.11 emite atributos ARIA (verificado en `bootstrap3` y
  `uni_form`): incompatible con lo que piden D3 y D6 → C8

> **Corrección:** una versión anterior de este anexo decía que `iva2.css` "no lo carga nadie".
> Es falso: lo carga `login_form.html:11`.

---

## Recursos

- **Django 1.11** (tu versión actual): `https://docs.djangoproject.com/en/1.11/`
  ⚠️ Verificá siempre que la URL diga `1.11`. Google te va a llevar a la documentación de la
  última versión y hay cosas que no existen en la tuya. Es la causa número uno de frustración
  trabajando con proyectos viejos
- **MDN** para HTML y CSS: `https://developer.mozilla.org/es/`
- **WCAG en lenguaje claro**: `https://www.w3.org/WAI/WCAG21/quickref/`
- **Patrones ARIA** (menús, modales, tabs): `https://www.w3.org/WAI/ARIA/apg/patterns/`
- **Lighthouse y Coverage**: ya vienen en las DevTools de Chrome, sin instalar nada
- Para el lector de pantalla: en macOS, **VoiceOver** se activa con `Cmd + F5`. Probar tu propia
  interfaz con los ojos cerrados durante cinco minutos enseña más sobre accesibilidad que
  cualquier artículo
