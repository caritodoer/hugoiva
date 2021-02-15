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
	
