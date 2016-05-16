Pedidos de Clínica
==================
Se presentará una pantalla que contendrá un listado con todos los *Pedidos de Clínica* que se encuentren registrados en el sistema hasta la fecha. 

.. image:: _static/pedidosclinica.png
   :align: center

Junto con el listado, se ofrecerán un conjunto de funcionalidades que permitirán manipular estos *Pedidos de Clínica*.
Estas funcionalidades son:

- :ref:`Alta Pedido <alta-pc>`
- :ref:`Ver Detalles <ver-detalles-pc>`
- :ref:`Ver Remitos <ver-remitos-pc>`
- :ref:`Formulario de Búsqueda <formulario-busqueda-pc>`

.. _alta-pc:

Alta Pedido
-----------
Si el usuario desea crear un nuevo *Pedido de Clínica*, deberá presionar el botón ``Alta``.

.. image:: _static/btnaltapedclin.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/altapedclin.png
   :align: center

En este punto el usuario deberá seleccionar la clínica que solicito el pedido, la obra social con la que trabaja, el médico auditor del pedido y la fecha en que fue solicitado a la empresa. A continuación deberá presionar el botón ``Crear Pedido``.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - La clínica ingresada no existe.
        - La fecha no existe.
        - La fecha ingresada esta fuera del rango válido.

Una vez presionado el botón ``Crear Pedido``, se mostrará la siguiente pantalla:

.. image:: _static/detallespedclin.png
   :align: center

Esta pantalla es la encargada de visualizar aquellos detalles que se irán asociando al *Pedido de Clínica*.

.. IMPORTANT::
    Los detalles de los *Pedidos de Clínica* contendrán solo aquellos medicamentos que se encuentren en stock.

Esta pantalla ofrece las siguientes funcionalidades:

    - :ref:`Agregar Detalle <agregar-detalle-pc>`
    - :ref:`Modificar Detalle <modificar-detalle-pc>`
    - :ref:`Eliminar Detalle <eliminar-detalle-pc>`
    - :ref:`Registrar Pedido <registrar-pedido-pc>`

.. _agregar-detalle-pc:

Agregar Detalle
+++++++++++++++
Si el usuario desea agregar un detalle al *Pedido de Clínica*, deberá presionar el botón ``Alta Detalle``.

.. image:: _static/btnadddetallepedclin.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/newdetallepedclin.png
   :align: center

En esta parte, se presentará un formulario que el usuario deberá completar para poder dar de alta un nuevo detalle.

.. ATTENTION:: 
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - No se seleccionó un medicamento.
        - No se ingresó una cantidad.
        - La cantidad ingresada no posee un formato correcto.
        - La cantidad ingresada es menor a cero.
        - La cantidad ingresada supera el stock disponible para el medicamento seleccionado.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar`` y el sistema se encargara de agregar el nuevo detalle al pedido.
El usuario podrá seguir dando de alta nuevos detalles, hasta donde considere necesario. Una vez que esto suceda deberá presionar el botón ``Cerrar`` y la ventana emergente desaparecerá.

.. _modificar-detalle-pc:

Modificar Detalle
+++++++++++++++++
Si el usuario desea modificar un detalle del *Pedido de Clínica*, deberá seleccionar el detalle que desea actualizar y presionar el botón ``Modificar Detalle``.

.. image:: _static/btnupddetallepedclin.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/upddetallepedclin.png
   :align: center

En esta parte, se presentará un formulario con la información actual del detalle y el usuario deberá actualizar aquella que considere necesaria.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - No se ingresó una cantidad.
        - La cantidad ingresada no posee un formato correcto.
        - La cantidad ingresada es menor a cero.
        - La cantidad ingresada supera el stock disponible para el medicamento seleccionado.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar`` y el sistema se encargará de actualizar la información de dicho detalle.

.. _eliminar-detalle-pc:

Eliminar Detalle
++++++++++++++++
Si el usuario desea eliminar un detalle del *Pedido de Clínica*, deberá seleccionar el detalle que desea eliminar y presionar el botón ``Baja Detalle``.

.. image:: _static/btndeldetallepedclin.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/deldetallepedclin.png
   :align: center

En esta parte el usuario deberá decidir si confirma la eliminación del detalle o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.

.. _registrar-pedido-pc:

Registrar Pedido
++++++++++++++++
Si el usuario desea registrar el *Pedido de Clínica*, deberá presionar el botón ``Registrar``.

.. image:: _static/btnregpedclin.png
   :align: center

.. ATTENTION::
    El sistema siempre validará que la información del pedido de clínica sea correcta. En caso de que esta información sea incorrecta el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - El pedido no contiene detalles
        - El pedido ya ha sido registrado anteriormente

Una vez presionado el botón ``Registrar``, el sistema se encargará de crear el *Pedido de Clínica* y se mostrará la siguiente ventana emergente (modal):

.. image:: _static/regpedclin.png
   :align: center

.. _ver-detalles-pc:

Ver Detalles
------------
Si el usuario desea ver los detalles de un *Pedido de Clínica*, deberá seleccionar el botón de **Acción** asociado a dicho pedido y presionar la pestaña ``Ver Detalles``.

.. image:: _static/btndetallespedclin.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/detallespedclin.png
   :align: center

Esta ventana mostrará todos los detalles del *Pedido de Clínica* seleccionado.

.. _ver-remitos-pc:

Ver Remitos
-----------
Si el usuario desea ver los remitos asociados a un *Pedido de Clínica*, deberá seleccionar el botón de **Acción** asociado a dicho pedido y presionar la pestaña ``Ver Remitos``.

.. image:: _static/btnremitospedclin.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/remitospedclin.png
   :align: center

Esta ventana mostrará todos los remitos vinculados al *Pedido de Clínica* seleccionado.

.. NOTE::
    En caso de que el pedido no tenga remitos asociados el sistema lo informará.

El usuario tendra la opción de visualizar un remito en PDF, presionanado el boton ``Descargar`` asociado a él.

Si se desea generar el remito en un pdf, el usuario deberá seleccionar el botón asociado al remito correspondiente y el sistema se encargará de generar el mismo.

.. _formulario-busqueda-pc:

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar sólo aquellos *Pedidos de Clínica* que cumplan con algunos criterios en específico, deberá utilizar el formulario de búsqueda.

.. image:: _static/busquedapedclin.png
   :align: center

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar los *Pedidos de Clínica* por clínica.
    - Búsqueda avanzada: permite buscar los *Pedidos de Clínica* por clínica, obra social, fecha desde y fecha hasta.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todos los *Pedidos de Clínica*.

El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Buscar``. El sistema visualizará aquellos *Pedidos de Clínica* que cumplan con todas las condiciones especificadas.

Si el usuario desea limpiar los filtros activos, deberá presionar el boton ``Limpiar``.

.. image:: _static/limpiarpedclin.png
   :align: center