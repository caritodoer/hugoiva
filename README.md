# hugoiva

## virtualenv
python3 -m venv env
env\Scripts\activate.bat

## Requisitos - Instalación
- Python3
- Django1.10
- Crispy forms : https://django-crispy-forms.readthedocs.io/en/latest/install.html
- import_export : http://django-import-export.readthedocs.io/en/latest/getting_started.html
- reportlab : https://pypi.org/project/reportlab/
'''
pip install django==1.10
pip install django-crispy-forms==1.11.0
pip install django-import-export==0.6.0
pip install reportlab==3.4
'''


## TASKS:
- en detalle del libro, que verifique que las fechas de fin no sea anterior a la de inicio u viceversa.











%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
en los botones de eliminar poner un window alert de  
"ELIMINACION EN CASCADA!!
Esta seguro que desea eliminar? Esta accion no se puede deshacer"

i_libro
i_dgr
cambiar botones para que abran en _blank
en tabla de libros:
* paginacion en tablas (hasta 20 registros)
* busqueda/filtro por encima de tablas que busque por empresa.

* pdf ---> ver formato de 
					- informes DGR (HUGO)
					- hoja libros

en form detalle: 
# boton agreagr cliente que abra un modal--falta guardar
# botones
	- guardar
	- guardar y cargar otro



que muestre el libro por el rango de fechas seleccionado? 








####################

* ABM usuarios + login/logout + permisos desde admin de django
templates:
- home:
	*menu
		-cliente
		-proveedor
		-libro

-cliente: listado
	-cargar
	-ver
-proveedor: listado
	-cargar
	-ver
-libro: listado
	-cargar
	-ver
	