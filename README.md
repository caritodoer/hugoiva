# hugoiva

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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


en detalle del libro, que verifique que las fechas de fin no sea anterior a la de inicio u viceversa.

que muestre el libro por el rango de fechas seleccionado? 








####################
PARA importaciones y exportaciones a excel se uso libreria django-import-export
http://django-import-export.readthedocs.io/en/latest/getting_started.html
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
	