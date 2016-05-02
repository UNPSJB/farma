Pedidos a Laboratorio
=====================
Se presentará una pantalla que contendrá un listado con todos los pedidos a laboratorio que se encuentren registrados en el sistema hasta la fecha. Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular estos pedidos.

CAPTURA

Estas funcionalidades son:

    - Alta de Pedido
    - Ver Detalles del Pedido
    - Ver Remitos del Pedido
    - Cancelar Pedido
    - Formulario de Búsqueda

Alta de Pedido
--------------
Si el usuario desea crear un nuevo pedido a laboratorio, deberá presionar el botón “Alta”. Una vez presionado este botón el sistema lo redirigirá a la siguiente pantalla.

CAPTURA

En este punto el usuario deberá seleccionar el laboratorio al cual desea realizarle el pedido y luego presionar el botón “Continuar”.

El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - No se seleccionó un laboratorio.

Una vez presionado el botón “Continuar”, se mostrará la siguiente pantalla:

CAPTURA

Esta pantalla es la encargada de visualizar los detalles que se correspondan con el pedido a laboratorio. 
De forma automática el sistema se encargara de buscar y agregar al pedido aquellos detalles de pedidos de farmacia que cumplan las siguientes condiciones:

    - Que contengan un medicamento producido por el laboratorio al cual se le está realizando el pedido.
    - Que haya stock suficiente para satisfacer el medicamento del detalle.
    - Que no se encuentren dentro de algún otro pedido a laboratorio.

Esta pantalla ofrece las siguientes funcionalidades para manipular el pedido a laboratorio:

    - Alta Detalle.
    - Modificación Detalle.
    - Baja Detalle.
    - Registrar Pedido.
    
Alta Detalle
++++++++++++
Si el usuario desea agregar un detalle al pedido a laboratorio, deberá presionar el botón de “Alta detalle”.

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
Si el usuario desea eliminar un detalle del pedido a laboratorio, deberá seleccionar el detalle que desea eliminar y presionar el botón de “Baja detalle”.

CAPTURA BOTÓN

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

En esta parte el usuario deberá decidir si confirma la eliminación del detalle o no. Si desea confirmar la eliminación deberá presionar el botón “Confirmar”, caso contrario, presionará el botón “Cancelar”.

Modificar Detalle
+++++++++++++++++
Si el usuario desea modificar un detalle del pedido a laboratorio, deberá seleccionar el detalle que desea actualizar y presionar el botón de “Modificar detalle”. Solo se podrán actualizar aquellos detalles que no se correspondan con pedidos de farmacia, es decir, aquellos que el sistema agrega automáticamente al ingresar a esta pantalla.

CAPTURA

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

En esta parte al usuario se le presentará un formulario con la información actual del detalle y deberá modificar la información que considere necesaria.
El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - No se ingresó una cantidad.
    - La cantidad ingresada no posee un formato correcto.
    - La cantidad ingresada es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón “Guardar” y el sistema se encargara de actualizar la información del detalle seleccionado.

Registrar Pedido
++++++++++++++++
Si el usuario desea registrar el pedido a laboratorio, deberá presionar el botón “Registrar”.

CAPTURA

El sistema siempre validará que la información del pedido a laboratorio sea correcta. En caso de que esta información sea incorrecta el sistema lo informará. 
En este punto, las posibles causas de errores son:

    - El pedido no contiene detalles
    - El pedido ya ha sido registrado anteriormente

Una vez presionado el botón “Registrar”, el sistema se encargará de crear el pedido a laboratorio  y se mostrará la siguiente ventana emergente (modal).

CAPTURA

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar solo aquellos pedidos a laboratorio que cumplan determinados criterios, deberá utilizar el formulario de búsqueda.

CAPTURA

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar los pedidos a laboratorio por laboratorio.
    - Búsqueda avanzada: permite buscar los pedidos a laboratorio por laboratorio y/o fecha desde y/o fecha hasta.

Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todos los pedidos a laboratorio.

Cancelar un Pedido
------------------
Si el usuario desea cancelar un pedido, deberá seleccionar el botón de “Acción” asociado al pedido a laboratorio y presionar la pestaña “Cancelar”. Solo se podrán cancelar aquellos pedidos a laboratorio que se encuentren en un estado “Pendiente”.

CAPTURA

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

En esta parte el usuario deberá decidir si confirma la eliminación del pedido a laboratorio. Si desea confirmar la eliminación deberá presionar el botón “Confirmar”, caso contrario, presionará el botón “Cancelar”.

Ver detalles del Pedido
-----------------------
Si el usuario desea ver los detalles de un pedido, deberá seleccionar el botón de “Acción” asociado al pedido a laboratorio y presionar la pestaña “Ver detalles”.

CAPTURA

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

Esta ventana mostrará todos los detalles que estén asociados al pedido a laboratorio seleccionado.

Ver Remitos del Pedido
----------------------
Si el usuario desea ver los remitos asociados a un pedido, deberá seleccionar el botón de “Acción” asociado al pedido a laboratorio y presionar la pestaña “Ver Remitos”.

CAPTURA

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

CAPTURA

Esta ventana mostrará todos los remitos  que estén asociados al pedido a laboratorio seleccionado.
En caso de que el pedido no tenga remitos asociados el sistema lo informará.

Si se desea generar el remito en un pdf, el usuario deberá seleccionar el botón asociado al remito correspondiente y el sistema se encargará de generar el mismo.

CAPTURA