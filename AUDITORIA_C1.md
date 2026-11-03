# Auditoría del estado visual y técnico — tarea C1

Fotografía del proyecto **antes** del rediseño. Documenta qué había, qué se usaba de verdad y
qué se decidió conservar. Es la línea de base contra la que se va a medir el resultado.

- **Proyecto:** hugoiva — gestión de libros de IVA compras/ventas (Django 1.11, Python 3.8)
- **Momento:** agosto de 2026, con las fases A y B terminadas y sin tocar todavía una línea de CSS
- **Herramientas:** pestaña Coverage de las DevTools de Chrome, inspección manual del código,
  cálculo de contraste WCAG, y pruebas a 360 px, 1440 px y ultrawide
- **Estado del código base:** el CSS y las plantillas son los originales de 2017; las fases A y B
  solo tocaron Python y configuración

> Las decisiones que salen de esta auditoría, con su razonamiento, están en `NOTAS_FASE_C.md`.
> El plan de trabajo está en `PLAN_DE_ACCION.md`, Fase C.

---

## Resumen ejecutivo

| Área | Hallazgo | Veredicto |
| --- | --- | --- |
| **CSS** | 4 hojas, ~7.100 líneas. Bootstrap se usa al **5,5%**, jQuery UI al **0%** | Se reescribe desde cero |
| **Tipografía** | 4 familias declaradas, 2 sin efecto real. 1,4 MB de fuentes que no usa nadie | Se rehace |
| **Color** | Paleta oscura coherente, pero **ningún par de texto llega a AAA**. Sin modo claro | Se rediseña la paleta |
| **Layout** | **Cero media queries** en todo el CSS propio. Sidebar de 240 px cableado | Se rehace mobile-first |
| **Formularios** | Generados por crispy_forms: sin ARIA, y la maquetación vive en Python | Se saca crispy |
| **Semántica HTML** | 16 `<h1>`, ningún `<h2>`. Sin jerarquía de encabezados | Se corrige |
| **Funcionalidad** | No existe forma de editar un usuario ni de cambiar la contraseña | Fuera de alcance, anotado |

---

## 1. CSS: qué se carga y cuánto se usa de verdad

`base.html` carga cuatro hojas de estilo. Medido con la pestaña **Coverage** de las DevTools
de Chrome sobre el home; las vistas de listado y de formulario dan valores muy parecidos.

| Hoja | Tamaño | Sin usar | Se usa |
| --- | --- | --- | --- |
| `bootstrap_modif.css` | 6.761 líneas (143 KB) | **94,5 %** | 5,5 % |
| `font-awesome.css` | 37 KB | **98 %** | 2 % |
| `jquery-ui.css` | 36 KB | **100 %** | nada |
| `iva.css` | 154 líneas (3 KB) | 37,2 % | 62,8 % |

**Lectura:** de las cuatro hojas, tres son prácticamente peso muerto. Se están descargando unos
**220 KB de CSS para usar el equivalente a unas diez reglas**. `jquery-ui.css` no se usa en
absoluto: está cargado por inercia.

`iva.css` —la única hoja escrita a mano en el proyecto— es la que mejor relación tiene, pero
aun así arrastra un tercio de reglas muertas.

### Una hoja más, y un 404

- **`iva2.css`** (148 líneas) solo la carga `login_form.html`. Es casi un duplicado de `iva.css`.
- **`login_form.html` y `logout_form.html` enlazan `/static/css/bootstrap.css`, que no existe.**
  Solo está en `static_root/`, la carpeta generada por `collectstatic` que se sacó del repositorio
  en la fase A. Verificado sirviendo el proyecto:

  | Petición | Respuesta |
  | --- | --- |
  | `/static/css/bootstrap.css` | **404** |
  | `/static/css/bootstrap_modif.css` | 200 |
  | `/static/css/iva2.css` | 200 |

  Consecuencia: **la pantalla de login —la primera que ve cualquiera— se muestra sin estilos**
  en cualquier clon nuevo del repositorio. Estaba roto desde antes de empezar este trabajo.

### JavaScript

Mismo diagnóstico. `base.html` carga cuatro archivos, e incluye **jQuery dos veces**
(`jquery.js` y `jquery-1.12.4.js`, líneas 36-37). Lo único que hace JavaScript hoy es:

1. El desplegable del menú lateral (`slideDown`)
2. Cuatro *datepickers* de jQuery UI (`altas`, `i_libro`, `i_dgr`, `v_libro`)
3. Un modal de Bootstrap en `altas.html` **que está muerto**: su cuerpo está vacío y el
   manejador apunta a un `#btnguardar` que no existe en ninguna parte (restos de
   `a_cp_modal.html`, plantilla eliminada en la fase B)

Los cuatro datepickers se reemplazan por `<input type="date">` nativo, que además es accesible
y funciona bien en móvil. Con eso, jQuery UI se queda sin ninguna razón para existir.

---

## 2. Tipografía

`iva.css` declara cuatro familias con `@font-face`. Tres de ellas tienen problemas.

| Familia | Dónde se aplica | Estado |
| --- | --- | --- |
| `Open-Sans` | `body` — toda la aplicación | Funciona |
| `Existence-Light` | `h1` | Funciona, pero se descarta (ver abajo) |
| `Ubuntu-B` | `h3` | Funciona, pero es invisible (ver abajo) |
| `Ubuntu-L` | **ninguna regla la usa** | Declarada y nunca aplicada |

### `Existence-Light`: bonita pero ilegible

Es la fuente de todos los `<h1>`, o sea de todos los títulos de página. Es muy fina y de bajo
contraste de trazo: a tamaños de interfaz cuesta leerla, y sobre fondo oscuro cuesta más
todavía. Es una fuente decorativa usada como fuente funcional. **Se descarta.**

### `Ubuntu-B`: el misterio resuelto

Durante la auditoría parecía que `Ubuntu-B` no cargaba, porque no se ve en ninguna pantalla.
No es un error de carga: el archivo existe y se sirve correctamente (`200 OK`).

La causa es otra, y es más interesante. La única regla que la aplica es `h3 { font-family:
Ubuntu-B; }` — y en todo el proyecto hay **un solo `<h3>`**:

```
templates/logout_form.html:24:  <h3 align="center">Hasta Pronto!!</h3>
```

Está en la pantalla de despedida, que es justamente la que se va a eliminar. La fuente
funcionaba perfectamente; simplemente no había casi nada a lo que aplicarse.

### 1,4 MB de fuentes que no usa nadie

`static/fonts/` pesa **6,8 MB**. Dentro hay trece archivos de la familia **Source Sans Pro**
(1,4 MB) que **no están referenciados en ningún CSS ni plantilla del proyecto**. Se copiaron en
2017 y ahí se quedaron.

También está la familia Ubuntu completa (18 archivos), de la que se declaran dos pesos y se usa
uno, en un solo elemento.

---

## 3. Color y contraste

La paleta actual es coherente y en la práctica es un tema oscuro, aunque nunca se declaró como
tal: no hay ningún `prefers-color-scheme`, ni modo claro, ni forma de alternar.

| Rol | Color |
| --- | --- |
| Fondo general | `#293949` |
| Fondo de nav y sidebar | `#23313f` |
| Texto general | `#ffffff` |
| Texto de navegación | `#aeb2b7` |
| Acento (hover, activo) | `#1abc9c` |

### Contraste medido

Ratios calculados según la fórmula de luminancia relativa de WCAG 2.1. Umbrales: **AA** exige
4,5:1 para texto normal y 3:1 para texto grande; **AAA** exige 7:1.

| Par | Ratio | AA | AAA |
| --- | --- | --- | --- |
| Texto general `#ffffff` sobre `#293949` | **11,83** | Pass | **Pass** |
| Enlaces del sidebar `#aeb2b7` sobre `#293949` | 5,55 | Pass | Fail |
| Submenús del sidebar `#aeb2b7` sobre `#23313f` | 6,23 | Pass | Fail |
| `navbar-brand` `#aeb2b7` sobre `#23313f` | 6,23 | Pass | Fail |
| Acento `#1abc9c` sobre `#293949` | 4,91 | Pass | Fail |
| Acento `#1abc9c` sobre `#23313f` | 5,51 | Pass | Fail |

**Lectura:** nada incumple el mínimo legal (AA), pero **solo el texto blanco principal llega a
AAA**. Toda la navegación se queda en la franja media: legible, pero lejos de cómoda. El acento
verde es el peor del conjunto (4,91), y es justamente el color que marca el estado activo y el
foco — el que más necesita destacar.

El objetivo del rediseño es subir toda la interfaz a AAA donde sea razonable, y como mínimo
alejar la navegación del límite.

### Una regla catastrófica, hoy inactiva

`.pie` (el pie de página) define texto blanco sobre `#cfd1d3`: **ratio 1,53:1**. Falla incluso
el umbral de texto grande. No se ve hoy porque el `<footer>` está comentado en `base.html`,
pero la regla sigue en la hoja esperando a que alguien la descomente.

---

## 4. Layout y comportamiento responsive

### El dato que lo explica todo

```bash
grep -c "@media" static/css/iva.css static/css/iva2.css
# iva.css  → 0
# iva2.css → 0
```

**Cero media queries en todo el CSS propio del proyecto.** No hay diseño responsive: hay un
diseño de escritorio, y lo que responde algo es lo que herede de Bootstrap 3 — que es
precisamente el 94,5 % que no se usa.

La causa concreta está en dos reglas de `iva.css`:

```css
.container { padding-left: 240px !important; }
body       { padding-right: 240px; padding-top: 70px; }
```

El hueco del menú lateral está **cableado a 240 px fijos**, con `!important`, sin ningún punto
de ruptura que lo desactive. Es la raíz de los tres problemas de abajo.

### Móvil (360 px) — roto

- La barra superior ocupa **dos tercios del alto de la pantalla**
- El menú lateral ocupa **más de la mitad del ancho**
- El contenido principal queda **tapado por la barra** y comprimido en lo que sobra
- El botón hamburguesa no funciona: dice `data-toggle="collpase"` —con la errata— y apunta a un
  `div` que está comentado más abajo

En la práctica, **la aplicación no se puede usar en un teléfono**.

### Escritorio (1440 px) — correcto

Es el único tamaño para el que se diseñó, y se nota: el contenido se ve bien y la relación
entre menú y contenido es razonable.

### Ultrawide — funcional pero incómodo

El contenido principal se mantiene centrado, pero el menú lateral queda pegado al borde
izquierdo, muy lejos. Recorrer con la vista de un extremo al otro cansa. Es un problema de
diseño, no de código: el patrón de barra superior fija más lateral fijo no escala a anchos
grandes.

### Reglas que apuntan a componentes que no funcionan

`iva.css` tiene bloques de `.sidebar` y `#leftside-navigation` heredados de una plantilla de
Bootstrap 3 que en este proyecto nunca se conectaron del todo. Estilan estados (`.active`,
submenús desplegables) que la aplicación no llega a producir.

---

## 5. Formularios: el caso `crispy_forms`

Los formularios del proyecto los genera **django-crispy-forms 1.11** con el pack `bootstrap3`.
Es el hallazgo con más consecuencias de toda la auditoría.

### Lo bueno, que hay que conservar

Crispy **sí hace bien una cosa importante**: cada control tiene su `<label>` correctamente
asociado mediante `for` ↔ `id`. Es el requisito de accesibilidad más básico de un formulario y
está cumplido en todas las pantallas.

> **Esto es un requisito de salida, no un detalle.** Al escribir los formularios a mano, la
> asociación `label` ↔ control tiene que seguir siendo correcta en el 100 % de los campos. Es
> muy fácil perderla sin darse cuenta, y sería un retroceso.

Crispy también marca los campos obligatorios con `class="requiredField"` y un asterisco.

### Lo malo: cero atributos ARIA

Ninguno de los template packs de crispy 1.11 emite un solo atributo ARIA. Verificado sobre los
dos candidatos:

```bash
grep "aria-" crispy_forms/templates/bootstrap3/field.html   # → sin resultados
grep "aria-" crispy_forms/templates/uni_form/field.html     # → sin resultados
```

Los errores de validación se pintan así:

```html
<p id="error_1_id_cuit" class="errorField">Este campo es obligatorio.</p>
```

Un párrafo suelto, visualmente cerca del campo pero **sin ninguna relación programática con
él**. Falta:

- **`aria-describedby`** en el control, apuntando al `id` del mensaje de error y del texto de
  ayuda. Sin esto, un lector de pantalla anuncia el campo sin decir qué salió mal
- **`aria-invalid="true"`** en el control con error. Sin esto, no hay forma de saber que el
  campo está en estado inválido salvo mirándolo
- **`role="alert"`** o una región `aria-live` para los errores que aparecen tras enviar

Consecuencia práctica: quien navega con lector de pantalla llega a un campo marcado en rojo,
no oye nada distinto, y no tiene forma de saber por qué el formulario no se envía.

### Lo peor: la maquetación vive dentro de Python

```python
# IVAcompras/forms.py:31-32
self.helper.label_class = "col-lg-3 col-sm-3"
self.helper.field_class = "col-lg-8 col-sm-8"
```

La grilla responsive del formulario —cuántas columnas ocupa la etiqueta, cuántas el campo, en
qué tamaños de pantalla— está escrita **en un archivo de formularios de Python**. Para cambiar
cómo se ve un formulario hay que editar código de servidor y volver a arrancar.

`DetalleForm` lleva esto al extremo: 17 campos organizados en dos columnas con un `<fieldset>`,
todo descrito como un árbol de `Layout(Div(Fieldset(Div(PrependedText(...)))))` en Python.

Es exactamente el acoplamiento que un sistema de diseño existe para romper: **presentación
dentro de la lógica de la aplicación**.

---

## 6. Semántica HTML y accesibilidad

Recuento de encabezados en las 17 plantillas:

| Elemento | Cantidad |
| --- | --- |
| `<h1>` | **16** |
| `<h2>` | **0** |
| `<h3>` | 1 |
| `<h4>` | 2 |

**No hay jerarquía de encabezados.** Prácticamente cada pantalla usa un único `<h1>` para su
título y nada más, y `login_form.html` tiene **dos `<h1>`** (el nombre del sistema y el título
de la pantalla). Los encabezados son el principal mecanismo de navegación para un lector de
pantalla: sin niveles intermedios, no hay forma de saltar por secciones dentro de una página.

Otros hallazgos estructurales, que se corrigen en las tareas C7 y D1:

- El elemento raíz es `<html >`, **sin atributo `lang`**. Fallo de WCAG nivel A
- El viewport **bloquea el zoom** (`user-scalable=no, maximum-scale=1.0`). Incumple WCAG 1.4.4:
  impide ampliar la página a quien tiene baja visión
- El `<title>` está **fijo** en "Gestion de IVA" para todas las páginas
- El contenido principal está en un `<div class="container">`, no en un `<main>`
- `login_form.html` y `logout_form.html` **no heredan de `base.html`**: son documentos completos
  con su propio `<head>`, lo que triplica los tres problemas anteriores
- Ninguna tabla tiene `<caption>` ni `scope` en sus `<th>`
- Los buscadores de los listados tienen `placeholder` pero **ningún `<label>`**
- Los submenús del lateral son `<a href="javascript:void(0);">`: un elemento que no navega pero
  abre y cierra algo **es un botón, no un enlace**. Hoy no se puede usar con teclado

---

## 7. Funcionalidad ausente y decisiones de producto

Hallazgos que no son de CSS pero salieron al recorrer la aplicación entera.

### No existe forma de editar un usuario

Se pueden **crear** usuarios (`/register/`) y **listar** (`usuarios.html`), pero no hay ninguna
vista para:

- Cambiar la contraseña propia
- Editar el nombre o el correo
- Desactivar o eliminar una cuenta

Hoy la única forma de cambiar una contraseña es por línea de comandos
(`python manage.py changepassword`). Para una aplicación con gestión de usuarios es una laguna
funcional grande.

**Decisión:** queda **fuera del alcance del rediseño**, anotado como trabajo futuro. Es
funcionalidad nueva, no rediseño de lo existente, y mezclarla con la Fase D confundiría el
"antes y después".

### La pantalla de despedida sobra

Al cerrar sesión, la aplicación lleva a `logout_form.html`: una pantalla que dice "Hasta
Pronto!!" con un enlace para volver al login. Es un patrón de 2010 que hoy se considera un paso
de más: la convención actual es **redirigir directamente al login**, con un mensaje de
confirmación si acaso.

**Decisión:** se elimina la pantalla y el logout redirige al login. Efecto colateral: desaparece
el único `<h3>` del proyecto y con él la última justificación de la fuente `Ubuntu-B`.

---

## 8. Decisión: qué se conserva y qué se va

| Elemento | Decisión | Cuándo |
| --- | --- | --- |
| `bootstrap_modif.css` (94,5 % sin usar) | **Fuera** | D8 |
| `jquery-ui.css` + `jquery-ui.js` (100 % sin usar) | **Fuera** | C9 |
| jQuery duplicado | **Fuera** (queda uno, y a revisar si hace falta) | C9 |
| `font-awesome.css` (98 % sin usar) | **Fuera.** Se sustituye por SVG en línea, solo los iconos que se usen | D |
| `iva.css` / `iva2.css` | **Fuera.** Se reescribe desde cero | D8 |
| Fuentes Source Sans Pro (1,4 MB) | **Fuera.** No las referencia nadie | C9 |
| `Existence-Light` | **Fuera.** Decorativa, poco legible | C4 |
| `Ubuntu-B` / `Ubuntu-L` | **Fuera.** Una se usa en un solo elemento que se elimina; la otra en ninguno | C4 |
| `crispy_forms` | **Fuera.** Los formularios se escriben a mano | C8 |
| `django-bootstrap3` | **Fuera.** Está instalada y no la carga ninguna plantilla | C9 |
| Modal muerto de `altas.html` | **Fuera** | C9 |
| Pantalla de despedida | **Fuera.** El logout redirige al login | D3 |
| Datepickers de jQuery UI | **Se sustituyen** por `<input type="date">` nativo | C9 |
| Paleta de color | **Se rediseña.** Se conserva el espíritu oscuro, con mejores contrastes | C4 |
| `<label>` asociados a cada control | **Se conserva.** Requisito de salida obligatorio | C8 |
| Edición de usuarios | **Fuera de alcance.** Anotado como trabajo futuro | — |

**Conclusión de la auditoría:** no se conserva prácticamente nada del CSS existente. Esto no es
una decisión tomada a la ligera sino la consecuencia directa de los números: cuando el 94,5 %
de tu hoja principal no se usa, mantenerla cuesta más que reescribirla. La reescritura arranca
de cero sobre custom properties propias, sin ningún framework.

---

## Anexo A: cómo se midieron estas cosas

Para poder repetir la medición después del rediseño y comparar.

**Cobertura de CSS** — DevTools de Chrome → menú de tres puntos → *More tools* → *Coverage* →
recargar la página con la grabación activa. Da bytes usados y sin usar por archivo.

**Contraste** — fórmula de luminancia relativa de WCAG 2.1 sobre los colores extraídos de
`iva.css`. Umbrales: AA = 4,5:1 (texto normal) y 3:1 (texto grande, ≥24 px o ≥18,66 px en
negrita); AAA = 7:1 y 4,5:1.

**Media queries** — `grep -c "@media" static/css/*.css`

**Encabezados** — `grep -roE "<h[1-5]([ >])" templates/`

**Archivos servidos** — `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8000/static/...`
con el servidor de desarrollo levantado.

**Anchos probados** — 360 px (móvil), 1440 px (escritorio) y ultrawide, con las capturas del
"antes" tomadas a 360 y 1440.

---

## Anexo B: por qué `base.html` no aparece en las DevTools

Durante la auditoría surgió esta duda, y conviene dejarla escrita porque es una confusión
frecuente cuando se trabaja con plantillas de servidor.

**`base.html` no aparece en las DevTools porque nunca llega al navegador.** Es una plantilla de
Django: vive solo en el servidor. Cuando pedís `/l_empresa/`, Django compone `base.html` +
`l_empresa.html` + los `includes`, y envía **un único documento HTML ya montado**. El navegador
recibe ese resultado y no tiene forma de saber de cuántos archivos salió.

Por eso, en la pestaña *Sources* vas a ver el documento por su **URL** (`/`, `/l_empresa/`), no
por el nombre de la plantilla. Y en *Coverage* aparecen los CSS y los JS —que sí son archivos
reales que el navegador descarga— pero nunca las plantillas.

No es un error ni tiene relación con los datepickers: es simplemente cómo funciona el
renderizado en servidor. Para ver qué plantilla generó qué, la herramienta es
**django-debug-toolbar**, que corre del lado del servidor.
