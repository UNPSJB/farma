Pedidos de Farmacia
===================
Se presentará una pantalla que contendrá un listado con todos los *Pedidos de Farmacia* que se encuentren registrados en el sistema hasta la fecha. 

.. image:: _static/pedidosfarmacia.png
   :align: center

Junto con el listado, se ofrecerán un conjunto de funcionalidades que permitirán manipular estos *Pedidos de Farmacia*. 
Estas funcionalidades son:

- :ref:`Alta Pedido <alta-pf>`
- :ref:`Ver Detalles <ver-detalles-pf>`
- :ref:`Ver Remitos <ver-remitos-pf>`
- :ref:`Formulario de Búsqueda <formulario-busqueda-pf>`

.. _alta-pf:

Alta Pedido
-----------
Si el usuario desea crear un nuevo *Pedido de Farmacia*, deberá presionar el botón ``Alta``.

.. image:: _static/btnaltapedfarm.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/altapedfarm.png
   :align: center
   
En este punto el usuario deberá seleccionar la fecha en que llegó el pedido y la farmacia que lo realizó. A continuación deberá presionar el botón ``Crear Pedido``.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - La farmacia ingresada no existe.
        - La fecha no existe.
        - La fecha ingresada esta fuera del rango válido.

Una vez presionado el botón ``Crear Pedido``, se mostrará la siguiente pantalla:

.. image:: _static/detallespedfarm.png
   :align: center

Esta pantalla es la encargada de visualizar aquellos detalles que se irán asociando al *Pedido de Farmacia*. 
La misma ofrece las siguientes funcionalidades:

    - :ref:`Agregar Detalle <agregar-detalle-pf>`
    - :ref:`Modificar Detalle <modificar-detalle-pf>`
    - :ref:`Eliminar Detalle <eliminar-detalle-pf>`
    - :ref:`Registrar Pedido <registrar-pedido-pf>`

.. _agregar-detalle-pf:

Agregar Detalle
+++++++++++++++
Si el usuario desea agregar un detalle al *Pedido de Farmacia*, deberá presionar el botón ``Alta Detalle``. 

.. image:: _static/btnadddetallepedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/newdetallepedfarm.png
   :align: center

En esta parte, se presentará un formulario que el usuario deberá completar para poder dar de alta un nuevo detalle.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - No se seleccionó un medicamento.
        - No se ingresó una cantidad.
        - La cantidad ingresada no posee un formato correcto.
        - La cantidad ingresada es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar`` y el sistema se encargara de agregar el nuevo detalle al pedido.
El usuario podrá seguir dando de alta nuevos detalles, hasta donde considere necesario. Una vez que esto suceda deberá presionar el botón ``Cerrar`` y la ventana emergente desaparecerá.

.. _modificar-detalle-pf:

Modificar Detalle
+++++++++++++++++
Si el usuario desea modificar un detalle del *Pedido de Farmacia*, deberá seleccionar el detalle que desea actualizar y presionar el botón ``Modificar Detalle``.

.. image:: _static/btnupddetallepedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/upddetallepedfarm.png
   :align: center

En esta parte, se presentará un formulario con la información actual del detalle y el usuario deberá actualizar aquella que considere necesaria.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - No se ingresó una cantidad.
        - La cantidad ingresada no posee un formato correcto.
        - La cantidad ingresada es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar`` y el sistema se encargará de actualizar la información de dicho detalle.

.. _eliminar-detalle-pf:

Eliminar Detalle
++++++++++++++++
Si el usuario desea eliminar un detalle del *Pedido de Farmacia*, deberá seleccionar el detalle que desea eliminar y presionar el botón ``Baja Detalle``.

.. image:: _static/btndeldetallepedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/deldetallepedfarm.png
   :align: center

En esta parte el usuario deberá decidir si confirma la eliminación del detalle o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.

.. _registrar-pedido-pf:

Registrar Pedido
++++++++++++++++
Si el usuario desea registrar el *Pedido de Farmacia*, deberá presionar el botón ``Registrar``.

.. image:: _static/btnregpedfarm.png
   :align: center

.. ATTENTION::
    El sistema siempre validará que la información del *Pedido a de Farmacia* sea correcta. En caso de que esta información sea incorrecta el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - El pedido no contiene detalles
        - El pedido ya ha sido registrado anteriormente

Una vez presionado el botón ``Registrar``, el sistema se encargará de crear el *Pedido de Farmacia* y se mostrará la siguiente ventana emergente (modal).

.. image:: _static/regpedfarm.png
   :align: center

.. _ver-detalles-pf:

Ver Detalles
------------
Si el usuario desea ver los detalles de un *Pedido de Farmacia*, deberá seleccionar el botón de **Acción** asociado a dicho pedido y presionar la pestaña ``Ver Detalles``.

.. image:: _static/btndetallespedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/verdetallespedfarm.png
   :align: center

Esta ventana mostrará todos los detalles del *Pedido de Farmacia* seleccionado.

.. _ver-remitos-pf:

Ver Remitos
-----------
Si el usuario desea ver los remitos asociados a un *Pedido de Farmacia*, deberá seleccionar el botón de **Acción** asociado a dicho pedido y presionar la pestaña ``Ver Remitos``.

.. image:: _static/btnremitospedfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/remitospedfarm.png
   :align: center

Esta ventana mostrará todos los remitos vinculados al *Pedido de Farmacia* seleccionado.

.. NOTE::
    En caso de que el pedido no tenga remitos asociados el sistema lo informará.

El usuario tendra la opción de visualizar un remito en PDF, presionanado el boton ``Descargar`` asociado a él.

.. _formulario-busqueda-pf:

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar sólo aquellos *Pedidos de Farmacia* que cumplan con algunos criterios en específico, deberá utilizar el formulario de búsqueda.

.. image:: _static/busquedapedfarm.png
   :align: center

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar los *Pedidos de Farmacia* por farmacia.
    - Búsqueda avanzada: permite buscar los *Pedidos de Farmacia* por farmacia, fecha desde, fecha hasta y estado del pedido.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todos los *Pedidos de Farmacia*.

El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Buscar``. El sistema visualizará aquellos *Pedidos de Farmacia* que cumplan con todas las condiciones especificadas.

Si el usuario desea limpiar los filtros activos, deberá presionar el boton ``Limpiar``.

.. image:: _static/limpiarpedfarm.png
   :align: center