Farmacias
=========
Se presentará una pantalla que contendrá un listado con todas las farmacias que se encuentren registradas en el sistema hasta la fecha. Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular estas farmacias.

CAPTURA

Estas funcionalidades son:

    - Alta de Farmacia
    - Baja de Farmacia
    - Modificacion de Farmacia
    - Formulario de Búsqueda
    
Alta de Farmacia
----------------
Si el usuario desea crear una nueva farmacia, deberá presionar el botón “Alta”. Una vez presionado este botón el sistema lo redirigirá a la siguiente pantalla.

CAPTURA

En este punto el usuario deberá ingresar los datos de la nueva farmacia. Estos datos son:
    
Campos Obligatorios:
::

    - Razón social
    - Cuit
    - Localidad
    - Dirección

Campos opcionales:
::

    - Nombre de encargado
    - Teléfono
    - Email
    
Luego de ingresar todos los datos, el usuario podra confirmar su grabación. Para esto cuenta con los botones “Guardar y volver” que redirige al listado inicial de una organización, y “Guardar y continuar” que mantiene la pantalla activa para crear una nueva farmacia.
    
El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - No se ingreso una razon social.
    - La razon social ingresada no posee un formato correcto.
    - No se ingreso un CUIT.
    - El CUIT ingresado no posee un formato correcto.
    - No se ingreso una localidad.
    - La localidad ingresada no posee un formato correcto.
    - No se ingreso una direccion.
    - La direccion ingresada no posee un formato correcto.
    - El nombre de encargado ingresado no posee un formato correcto.
    - El telefono ingresado no posee un formato correcto.
    - El email ingresado no posee un formato correcto.
    
Baja de Farmacia
----------------
Si el usuario desea eliminar una farmacia, deberá hacer “click” en la fila correspondiente y presionar el botón de “Acción” y seleccionar la opción eliminar.

CAPTURA BOTÓN

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

En esta parte el usuario deberá decidir si confirma la eliminación de la farmacia. Si desea confirmar la eliminación deberá presionar el botón “Confirmar”, caso contrario, presionará el botón “Cancelar”.

Modificacion de Farmacia
------------------------
Si el usuario desea modificar una farmacia, deberá hacer “click” en la fila correspondiente y presionar el botón de “Acción” y seleccionar la opción modificar.
Una vez presionado este botón el sistema lo redirigirá a la siguiente pantalla.

CAPTURA

En esta parte el usuario se le presentará un formulario con la información modificable de la farmacia, y podra actualizar la información que considere necesaria.

Una vez modificado el formulario, el usuario deberá presionar el botón “Guardar cambios” y el sistema se encargara de actualizar la información de la farmacia seleccionada.

El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - No se ingreso una localidad.
    - La localidad ingresada no posee un formato correcto.
    - No se ingreso una direccion.
    - La direccion ingresada no posee un formato correcto.
    - El nombre de encargado ingresado no posee un formato correcto.
    - El telefono ingresado no posee un formato correcto.
    - El email ingresado no posee un formato correcto.

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar solo aquellas farmacias que cumplan determinados criterios, deberá utilizar el formulario de búsqueda.

CAPTURA

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar las farmacias por razon social.
    - Búsqueda avanzada: permite buscar las farmacias por razon social y/o localidad.

Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todos los pedidos de farmacia.