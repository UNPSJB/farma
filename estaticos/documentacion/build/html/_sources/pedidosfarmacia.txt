Pedidos de Farmacia
===================
Se presentará una pantalla que contendrá un listado con todos los pedidos de farmacia que se encuentren registrados en el sistema hasta la fecha. Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular estos pedidos.

CAPTURA

Estas funcionalidades son:

    - Alta de Pedido
    - Ver detalles del Pedido
    - Ver Remitos del Pedido
    - Formulario de Búsqueda

Alta de Pedido
--------------
Si el usuario desea crear un nuevo pedido de farmacia, deberá presionar el botón “Alta”. Una vez presionado este botón el sistema lo redirigirá a la siguiente pantalla

CAPTURA

En este punto el usuario deberá seleccionar la farmacia que solicito el pedido y la correspondiente fecha en que fue solicitado a la empresa; luego presionar el botón “Crear pedido”.

El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - La farmacia ingresada no existe.
    - La fecha no es válida.
    - La fecha es incorrecta en un sentido “temporal”

Una vez presionado el botón “Crear pedido”, se mostrará la siguiente pantalla:

CAPTURA

Esta pantalla es la encargada de visualizar los detalles que se correspondan con el pedido de farmacia. 
Esta pantalla ofrece las siguientes funcionalidades para manipular el pedido de farmacia:

    - Alta Detalle.
    - Modificación Detalle.
    - Baja Detalle.
    - Registrar Pedido.


Alta Detalle
++++++++++++
Si el usuario desea agregar un detalle al pedido de farmacia, deberá presionar el botón de “Alta detalle”. 

CAPTURA BOTÓN

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

En esta parte el usuario se le presentará un formulario y deberá ingresar la información solicitada para dar de alta un nuevo detalle.
El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - No se seleccionó un medicamento.
    - No se ingresó una cantidad.
    - La cantidad ingresada no posee un formato correcto.
    - La cantidad ingresada es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón “Guardar” y el sistema se encargara de agregar el nuevo detalle al pedido.
El usuario podrá seguir dando de alta nuevos detalles, hasta donde considere necesario. Una vez que esto suceda deberá presionar el botón “Cerrar” y la ventana emergente desaparecerá.

Baja Detalle
++++++++++++
Si el usuario desea eliminar un detalle del pedido de farmacia, deberá seleccionar el detalle que desea eliminar y presionar el botón de “Baja detalle”.

CAPTURA BOTÓN

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

En esta parte el usuario deberá decidir si confirma la eliminación del detalle o no. Si desea confirmar la eliminación deberá presionar el botón “Confirmar”, caso contrario, presionará el botón “Cancelar”.

Modificar Detalle
+++++++++++++++++
Si el usuario desea modificar un detalle del pedido de farmacia, deberá seleccionar el detalle que desea actualizar y presionar el botón de “Modificar detalle”.

CAPTURA

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

En esta parte el usuario se le presentará un formulario con la información actual del detalle y deberá modificar la información que considere necesaria.
El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - No se ingresó una cantidad.
    - La cantidad ingresada no posee un formato correcto.
    - La cantidad ingresada es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón “Guardar” y el sistema se encargara de actualizar la información del detalle seleccionado.

Registrar Pedido
++++++++++++++++
Si el usuario desea registrar el pedido de farmacia, deberá presionar el botón “Registrar”.

CAPTURA

El sistema siempre validará que la información del pedido A de farmacia sea correcta. En caso de que esta información sea incorrecta el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - El pedido no contiene detalles
    - El pedido ya ha sido registrado anteriormente

Una vez presionado el botón “Registrar”, el sistema se encargará de crear el pedido de farmacia y se mostrará la siguiente ventana emergente (modal).

CAPTURA

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar solo aquellos pedidos de farmacia que cumplan determinados criterios, deberá utilizar el formulario de búsqueda.

CAPTURA

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar los pedidos de farmacia por farmacia.
    - Búsqueda avanzada: permite buscar los pedidos de farmacia por farmacia y/o  fecha desde y/o fecha hasta y/o estado del pedido.

Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todos los pedidos de farmacia.

Ver detalles del Pedido
-----------------------
Si el usuario desea ver los detalles de un pedido, deberá seleccionar el botón de “Acción” asociado al pedido de farmacia y presionar la pestaña “Ver detalles”.

CAPTURA

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

Esta ventana mostrará todos los detalles que estén asociados al pedido de farmacia.

Ver Remitos del Pedido
----------------------
Si el usuario desea ver los remitos asociados a un pedido, deberá seleccionar el botón de “Acción” asociado al pedido de farmacia y presionar la pestaña “Ver Remitos”.

CAPTURA

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

Esta ventana mostrará todos los remitos  que estén asociados al pedido de farmacia.

En caso de que el pedido no tenga remitos asociados el sistema lo informará.

Si se desea generar el remito en un pdf, el usuario deberá seleccionar el botón asociado al remito correspondiente y el sistema se encargará de generar el mismo.

CAPTURA