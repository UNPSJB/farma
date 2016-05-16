Medicamentos
============
Se presentará una pantalla que contendrá un listado con todos los *Medicamentos* que se encuentren registrados en el sistema hasta la fecha. 

.. image:: _static/medicamentos.png
   :align: center

Junto con el listado, se ofrecerán un conjunto de funcionalidades que permitirán manipular estos *Medicamentos*

Estas funcionalidades son:

    - :ref:`Alta Medicamento <alta-medicamento>`
    - :ref:`Modificar Stock Mínimo <modificar-stock-minimo>`
    - :ref:`Modificar Precio Venta <modificar-precio-venta>`
    - :ref:`Eliminar Medicamento <eliminar-medicamento>`
    - :ref:`Ver Lotes <ver-lotes>`
    - :ref:`Formulario de Búsqueda <formulario-busqueda-medicamento>`

.. _alta-medicamento:

Alta Medicamento
----------------
Si el usuario desea crear un nuevo *Medicamento*, deberá presionar el botón ``Alta``. 

.. image:: _static/btnaltamed.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/altamed.jpg
   :align: center

En esta parte al usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta un nuevo *Medicamento*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

    - Uno o más campos vacíos.
    - El código de barras del medicamento ya existe.
    - La monodroga ingresada no existe.
 
Una vez completado el formulario, el usuario tendrá dos opciones: 
    
    - Presionar el botón ``Guardar y Volver``.
    - Presionar el botón ``Guardar y Continuar``.

El botón ``Guardar y Volver`` permite guardar el *Medicamento* en el sistema y volver a la pantalla 
principal de medicamentos.

El botón ``Guardar y Continuar`` permite guardar el *Medicamento* en el sistema y seguir dando de alta nuevos *Medicamentos*.

.. _modificar-stock-minimo:

Modificar Stock Mínimo
----------------------
Si el usuario desea modificar el stock mínimo de un *Medicamento*, deberá seleccionar el botón de **Acción** asociado al *Medicamento* y presionar la pestaña ``Modificar Stock Mínimo``.

.. image:: _static/modifstockmin.png
   :align: center

Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/modifstockmed.png
   :align: center

En esta parte el usuario se le presentará un formulario y deberá actualizar la información del stock asociado al *Medicamento*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - No se ingresó un stock mínimo.
        - El stock mínimo ingresado no posee un formato correcto.
        - El stock mínimo ingresado es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar Cambios`` y el sistema se encargará de actualizar el stock mínimo del *Medicamento* seleccionado.

.. _modificar-precio-venta:

Modificar Precio de Venta
-------------------------
Si el usuario desea modificar el precio de venta de un *Medicamento*, deberá seleccionar el botón de **Acción** asociado al *Medicamento* y presionar la pestaña ``Modificar Precio Venta``.

.. image:: _static/modifprecioventa.png
   :align: center

Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/modifpreciomed.png
   :align: center

En esta parte el usuario se le presentará un formulario y deberá actualizar la información del precio de venta asociado al *Medicamento*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - No se ingresó un precio de venta.
        - El precio de venta ingresado no posee un formato correcto.
        - El precio de venta ingresado es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar Cambios`` y el sistema se encargará de actualizar el precio de venta del *Medicamento* seleccionado.

.. _eliminar-medicamento:

Eliminar Medicamento
--------------------
Si el usuario desea eliminar un *Medicamento*, deberá seleccionar el botón de **Acción** asociado al *Medicamento* y presionar la pestaña ``Eliminar``.

.. image:: _static/btneliminarmed.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/eliminarmed.png
   :align: center

En esta parte el usuario deberá decidir si confirma la eliminación del *Medicamento* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.

.. NOTE::
    Aquellos *Medicamentos* que cumplan las siguientes condiciones **NO** podrán ser eliminados:

        - Esten pendientes parcial o totalmente en un Pedido a Laboratorio.
        - Esten pendientes parcial o totalmente en un Pedido de Farmacia.
        - Posean lotes activos.

    El sistema se encargará de informar al usuario las razones por las cuales el *Medicamento* seleccionado no puede eliminarse. En dicho caso, el sistema mostrara una ventana emergente (modal) como esta:
    
    .. image:: _static/fallaeliminarmed.png
       :align: center

.. _ver-lotes:

Ver Lotes
---------
Si el usuario desea ver los lotes de un *Medicamento*, deberá seleccionar el botón de **Acción** asociado al *Medicamento* y presionar la pestaña ``Ver Lotes``.

.. image:: _static/verlotes.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/lotesmed.png
   :align: center

Esta ventana mostrará todos los lotes que estén asociados al *Medicamento*.

.. NOTE::
    En caso de que el *Medicamento* seleccionado no posea lotes activos, el sistema se encargará de mostrar la siguiente ventana emergente (modal):

    .. image:: _static/nolotes.png
       :align: center

.. _formulario-busqueda-medicamento:

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar sólo aquellos *Medicamentos* que cumplan con algunos criterios en específico, deberá utilizar el formulario de búsqueda.

.. image:: _static/busquedamed.png
   :align: center

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar los *Medicamentos* por nombre fantasía.
    - Búsqueda avanzada: permite buscar los *Medicamentos* por nombre fantasía y laboratorio.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todos los *Medicamentos*.

El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Buscar``. El sistema visualizará aquellos *Medicamentos* que cumplan con todas las condiciones especificadas.

Si el usuario desea limpiar los filtros activos, deberá presionar el boton ``Limpiar``.

.. image:: _static/limpiarbusquedamed.png
   :align: center