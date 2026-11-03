# Notas de la Fase C — decisiones y por qués

Documento de discusión, no de tareas. Las tareas están en `PLAN_DE_ACCION.md`, Fase C.
Esto es el razonamiento que hay detrás de esas tareas, para cuando dentro de tres meses
te preguntes "¿y por qué habíamos decidido esto?".

Fecha: agosto 2026, al cerrar la Fase B y antes de tocar una sola línea de CSS.

---

## 1. Estado del proyecto al arrancar la Fase C

Lo único pendiente era mergear `refactor` a `master` (13 commits) — que es la tarea C0.

---

## 2. Crispy: ¿obliga a usar Bootstrap? — No, pero la respuesta interesante es otra

### El dato técnico

Crispy no depende de Bootstrap en absoluto. Lo que crispy tiene es un **template pack**: un
conjunto de plantillas Django que deciden qué HTML se escupe alrededor de cada campo. La
versión instalada (1.11) trae cuatro packs incluidos:

```
env/lib/python3.8/site-packages/crispy_forms/templates/
├── bootstrap
├── bootstrap3      ← el que usa hoy el proyecto
├── bootstrap4
└── uni_form        ← este no tiene nada de Bootstrap
```

Cambiando una línea de `settings.py` (`CRISPY_TEMPLATE_PACK = "uni_form"`) crispy deja de
emitir clases de Bootstrap hoy mismo. Así que la respuesta literal a la pregunta es:
**no, crispy no obliga a Bootstrap.**

### Pero eso no es lo que importa

Miré el HTML que generan `uni_form/field.html` y `bootstrap3/field.html`. Los dos tienen el
mismo problema:

```bash
grep "aria-" .../crispy_forms/templates/bootstrap3/field.html   # → nada
grep "aria-" .../crispy_forms/templates/uni_form/field.html     # → nada
```

**Cero atributos ARIA en cualquiera de los packs.** Los errores se pintan como un
`<p class="errorField">` suelto, sin `aria-describedby` que lo conecte al campo, sin
`aria-invalid`. Es markup de 2013.

Y resulta que el plan, en D3 y D6, pide exactamente eso: errores asociados con
`aria-describedby`, obligatorios marcados de forma redundante, `inputmode` correcto.
**Ningún pack de crispy 1.11 da eso.** Habría que pelearse con la librería para conseguir
lo que la Fase D define como criterio de "hecho".

### El segundo problema, más de fondo

Dónde vive hoy la maquetación:

```python
# IVAcompras/forms.py:31-32
self.helper.label_class = "col-lg-3 col-sm-3"
self.helper.field_class = "col-lg-8 col-sm-8"
```

Eso es la grilla de Bootstrap 3 **escrita en Python**. El diseño responsive está definido en
un archivo de formularios. Ese es justo el acoplamiento que la Fase C existe para romper.

### Las tres opciones

|                                                        | Qué implica                                                                                                                       | Veredicto                             |
| ------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| **A. Sacar crispy**                                    | Un include `campo.html` de ~25 líneas + un `{% for field in form %}`. Se borran ~80 líneas de `forms.py`. Control total del HTML. | ✅ **Esta**                           |
| **B. Template pack propio**                            | Crear ~10 plantillas replicando la API interna de crispy. Aprendés crispy, no CSS.                                                | ❌ Esfuerzo mal invertido             |
| **C. Quedarse con bootstrap3 y re-estilar sus clases** | Escribir a mano `.form-group{}`, `.form-control{}`, `.col-lg-3{}`…                                                                | ❌ Terminás reimplementando Bootstrap |

### Por qué la A

Cuatro argumentos, de más a menos fuerte:

1. **Es lo que pedía el propio plan.** D3 ya decía "empezá a mano en esta pantalla para
   entender qué generaba crispy". La conclusión de ese ejercicio, con lo de arriba a la
   vista, iba a ser "a mano es mejor".
2. **La accesibilidad no es negociable en la Fase D**, y ningún pack la da.
3. **Ahorra trabajo en la Fase F.** El plan ya lo anotaba: crispy 2.x separó los packs a
   paquetes aparte, es una migración rota. Sacándolo ahora, ese renglón desaparece de la
   Fase F. Menos deuda por adelantado.
4. **Es el ejercicio correcto para el portfolio.** "Escribí un template de campo accesible y
   reutilizable" es una frase de perfil de diseño. "Configuré crispy" no.

### Lo que cuesta (el precio, a la vista)

Son **3 plantillas** tocadas (`login_form.html`, `logout_form.html`, `altas.html`) y
**5 formularios** en dos archivos.

El caso difícil es **`DetalleForm`**: 17 campos, layout en dos columnas, un `<fieldset>`
"Valores" y diez `PrependedText` con el "$" adelante. Hacerlo a mano son ~60 líneas de HTML
en una plantilla. Pero fijate que ese HTML es _más_ legible que el
`Layout(Div(Fieldset(Div(PrependedText(...)))))` de ahora, y es justo donde vas a querer
decidir el diseño con las manos.

---

## 3. Tailwind vs CSS crudo

**Recomendación: CSS crudo.** Y no por purismo — por tres razones concretas de _este_
proyecto:

**1. Tailwind taparía justo lo que querés mostrar.** El objetivo de la Fase C es un sistema
de diseño con tokens. Tailwind _ya trae_ un sistema de diseño: su escala de espaciado, su
escala tipográfica, su paleta. Si lo usás, la decisión de diseño ya está tomada por otro y
tu trabajo se convierte en elegir entre `p-4` y `p-6`. Alguien que abre tu CSS y ve
`--espacio-3: 12px` dentro de una escala pensada, ve criterio. Si ve
`class="px-4 py-2 rounded-lg"`, ve que sabés Tailwind. Son dos señales distintas, y acá
querés la primera.

**2. Rompe la promesa del README.** En la Fase A escribiste un README que dice: clonás,
`pip install`, `migrate`, `loaddata`, `runserver`. Tailwind mete Node y un paso de build.
Se puede hacer sin npm (el CLI standalone es un binario suelto), pero igual sumás
"descargate este ejecutable y corré `--watch` en otra terminal" a un proyecto cuyo argumento
de venta es que cualquiera lo levanta en dos minutos.

**3. El CSS de 2026 ya no necesita ayuda.** Custom properties, Grid, `clamp()`,
`:focus-visible`, `:has()`, anidamiento nativo. La mitad de lo que hacía indispensable a un
framework en 2017 hoy viene en el navegador. Estás reemplazando **6.761 líneas** de Bootstrap
por unas 400-500 tuyas. Eso, contado en el README, es una historia buenísima.

### El contraargumento honesto, porque existe

Tailwind aparece en muchísimas ofertas de trabajo. Si eso pesa, el consejo es no resolverlo
acá: este proyecto es la pieza de diseño. Tailwind se demuestra mejor en un proyecto chico y
nuevo, sin 6.761 líneas de Bootstrap 3 abajo peleando.

---

## 4. ¿Otra librería de componentes?

Respuesta corta: **no, salvo una excepción que no es una librería.**

Cualquier framework de componentes (Bulma, Bootstrap 5, Pico, DaisyUI, Shoelace) deja el
proyecto en el mismo lugar donde está: con el diseño de otra persona encima. Cambiar
Bootstrap 3 por Bootstrap 5 no es rediseñar, es actualizar. Y para un portfolio de diseño,
"se nota que es Bulma" es exactamente el comentario que no querés.

Además, acá no hay React: son plantillas Django renderizadas en el servidor. Las librerías
modernas de componentes asumen un framework JS. Shoelace/Web Awesome funcionan con web
components sin framework, pero traen su propio JS y su propia capa de theming — otra vez, el
diseño de otro.

**La excepción que sí vale la pena mirar: [Open Props](https://open-props.style/).** No es
una librería de componentes: son literalmente custom properties de CSS — escalas de
espaciado, tipografía, sombras, colores, curvas de animación. Cero componentes, cero opinión
sobre cómo se ve un botón.

La sugerencia **no es instalarlo, sino abrirlo y mirarle las escalas** mientras hacés los
tokens (tarea C4). Es una referencia excelente de cómo alguien que sabe construye una escala
tipográfica o de sombras. Se copia el criterio, no el archivo.

---

## 5. Figma, capturas y orden de trabajo

Sobre los bocetos: **sí, y antes de escribir CSS.** Pero cuidado con el error clásico, que es
hacer un Figma bonito de escritorio y descubrir en el navegador que en móvil no cierra. Dos
cosas que sirven:

- **Empezá los bocetos por el ancho de móvil (360 px).** Es más difícil y es lo que fuerza
  las decisiones reales: qué columnas de las 9 de `l_cli_pro` sobreviven, dónde va la
  navegación con 6 secciones. Lo de escritorio después sale casi solo.
- **No hace falta bocetar las 17 pantallas.** Con `base.html` + un listado + un formulario +
  un detalle tenés los cuatro patrones; el resto son variaciones. Bocetar quince pantallas
  antes de tocar código es cómo se muere un rediseño.

Sobre las capturas del "antes": sacalas **a dos anchos, 1440 px y 360 px**. Las de 360 son
las que mejor van a contar el "antes y después", porque el menú móvil hoy está roto (el typo
`data-toggle="collpase"` de D2) y eso se ve en la captura.

---

## 6. Hallazgos nuevos de esta revisión

Cosas que aparecieron mirando el proyecto para responder lo anterior. Todas verificadas
ejecutando, y todas ya incorporadas como tareas en el plan.

### `django-bootstrap3` está instalado y no lo usa nadie

```python
# IVA/settings.py:67
"bootstrap3",   # django-bootstrap3 12.0.3
```

Está en `INSTALLED_APPS` y **ninguna plantilla la carga**. Cero `{% load bootstrap3 %}`,
cero `{% bootstrap_form %}`. Se borra de `settings.py` y de `requirements.txt` sin tocar
nada más. Regalo.

### La pantalla de login carga una hoja de estilos que no existe

`login_form.html:10` y `logout_form.html:10` enlazan `/static/css/bootstrap.css`. Ese
archivo **no existe en `static/`**. Solo existe en `static_root/`, que es la salida generada
por `collectstatic` y que en la Fase A5 sacaste del repo.

Comprobado levantando el servidor:

| archivo                           | respuesta |
| --------------------------------- | --------- |
| `/static/css/bootstrap.css`       | **404**   |
| `/static/css/bootstrap_modif.css` | 200       |
| `/static/css/iva2.css`            | 200       |

O sea: **la primera pantalla que ve cualquiera está rota desde antes de que empezaras.**
En cuanto alguien clone el repo, se ve sin estilos. Sacá la captura del login _tal como está_
antes de arreglarlo — es material honesto para el "antes y después".

### El plan se equivocaba con `iva2.css`

El anexo decía "148 líneas que no carga nadie". Falso: lo carga `login_form.html:11`.
Corregido en el plan.

### Queda un modal muerto en `altas.html`

`altas.html:15-29` tiene un modal `#acpmodal` con un cuerpo vacío (`<div id="aca">`), y el JS
de la línea 41 engancha un click a `#btnguardar`, **que no existe en ninguna parte**. Son los
restos de `a_cp_modal.html`, la plantilla que borraste en B4. Código muerto que sobrevivió a
la limpieza.

### `login_form.html` y `logout_form.html` no heredan de `base.html`

Son documentos HTML completos, con su propio `<head>` duplicado (y con los mismos tres
problemas de accesibilidad que C7 arregla en `base.html`: sin `lang`, viewport que bloquea el
zoom, `<title>` fijo). Al rediseñar hay que decidir si se pasan a `{% extends %}` con un
bloque para el layout centrado, o si se quedan sueltas. Recomendación: heredar. Un `<head>`
correcto escrito una vez es mejor que tres copias que hay que mantener sincronizadas.

### jQuery está cargado dos veces

`base.html:36-37` carga `jquery.js` **y** `jquery-1.12.4.js`. Lo real que usa JS hoy es: el
`slideDown` del aside, los `datepicker()` de jQuery UI (en `altas`, `i_libro`, `i_dgr`,
`v_libro`) y el modal de Bootstrap en `altas.html` — que acabamos de ver que está muerto.

Los datepickers se reemplazan con `<input type="date">` nativo, que además es accesible y
funciona bien en móvil. Eso deja a jQuery UI (36 KB de CSS + su JS) sin ninguna razón para
existir.

---

## 7. Una advertencia de secuencia

**`bootstrap_modif.css` no se borra en la Fase C.** Se borra en D8, y hay una razón: las 17
plantillas siguen llenas de `class="container"`, `col-md-10`, `btn btn-default`,
`glyphicon-chevron-left`. El día que quites esa hoja, todas se caen a la vez.

El orden correcto es: primero las plantillas dejan de usar clases de Bootstrap (Fase D, una
pantalla por vez, con la app funcionando en cada paso), y **al final** se borra la hoja y se
comprueba que no pasó nada.

Lo que sí sale en la Fase C es todo lo que se puede quitar **sin romper nada visible**:
la app `bootstrap3` (muerta), crispy (porque bloquea el diseño de los formularios), jQuery UI
y el jQuery duplicado.

---

## 8. Resumen de decisiones

| Pregunta                                | Decisión                                               |
| --------------------------------------- | ------------------------------------------------------ |
| ¿Refactorizar algo antes de la Fase C?  | No. Solo mergear `refactor` → `master`                 |
| ¿Crispy obliga a Bootstrap?             | No, pero igual lo sacamos: sus packs no son accesibles |
| ¿Tailwind o CSS crudo?                  | CSS crudo con custom properties                        |
| ¿Alguna librería de componentes?        | Ninguna. Open Props solo como referencia visual        |
| ¿Cuándo se borra `bootstrap_modif.css`? | En D8, no antes                                        |
