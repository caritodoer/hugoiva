# hugoiva

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

* paginacion en tablas (hasta 20 registros)
* busqueda/filtro por encima de tablas
* pdf ---> ver formato de 
					- informes DGR (HUGO)
					- hoja libros
* ABM usuarios + login/logout + permisos desde admin de django

en form detalle: 
# boton agreagr cliente que abra un modal--falta guardar
# botones
	- guardar
	- guardar y cargar otro

PARA importaciones y exportaciones a excel se uso libreria django-import-export
http://django-import-export.readthedocs.io/en/latest/getting_started.html










####################
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
	