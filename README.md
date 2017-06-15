# hugoiva

#####################
en home.html la tabla de los libros tiene que mostrar
	cliente			periodo
con un link en el periodo que redirige a la carga de ese cliente para ese periodo.
se muestra todo lo cargado en ese libro y se permite seguir cargando items o eliminar items (como un modificar)

#####################
dos models seprados:

encabezado:
-periodo
-cliente

detalle factura
- fecha
-factura n°
-tipo
-proveedor
-cuit
...
-total facturado

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
	