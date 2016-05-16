Farmacias
=========
Se presentará una pantalla que contendrá un listado con todas las *Farmacias* que se encuentren registradas en el sistema hasta la fecha. 

.. image:: _static/monodrogas.png
   :align: center

Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular estas *Farmacias*.

Estas funcionalidades son:

    - :ref:`Alta Farmacia <alta-farmacia>`
    - :ref:`Modificar Farmacia <modificar-farmacia>`
    - :ref:`Eliminar Farmacia <eliminar-farmacia>`
    - :ref:`Formulario de Búsqueda <formulario-busqueda-farmacia>`
    
.. _alta-farmacia:

Alta Farmacia
-------------
Si el usuario desea crear una nueva *Farmacia*, deberá presionar el botón ``Alta``. 

.. image:: _static/btnaltafarm.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/altafarm.png
   :align: center

En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Farmacia*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos obligatorios vacíos.
        - Uno o más campos con un formato incorrecto.
        - El CUIT ingresado ya se encuentra asociado a otra organización.
     
Una vez completado el formulario, el usuario tendrá dos opciones: 
    
    - Presionar el botón ``Guardar y Volver``.
    - Presionar el botón ``Guardar y Continuar``.

El botón ``Guardar y Volver`` permite guardar la *Farmacia* en el sistema y volver a la pantalla 
principal de *Farmacias*..

El botón ``Guardar y Continuar`` permite guardar la *Farmacia* en el sistema y seguir dando de alta nuevas *Farmacias*.

.. _modificar-farmacia:

Modificar Farmacia
------------------
Si el usuario desea modificar los datos de una *Farmacia*, deberá seleccionar el botón de **Acción** asociado a la *Farmacia* y presionar la pestaña ``Modificar``.

.. image:: _static/btnmodificarfarm.png
   :align: center

Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/modificarfarm.png
   :align: center

En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Farmacia*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos obligatorios vacíos.
        - Uno o más campos con un formato incorrecto.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar Cambios`` y el sistema se encargara de actualizar los datos de la *Farmacia* seleccionada.


.. _eliminar-farmacia:
   
Eliminar Farmacia
-----------------
Si el usuario desea eliminar una *Farmacia*, deberá seleccionar el botón de **Acción** asociado a la *Farmacia* y presionar la pestaña ``Eliminar``.

.. image:: _static/btneliminarfarm.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/eliminarfarm.png
   :align: center

En esta parte el usuario deberá decidir si confirma la eliminación de la *Farmacia* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.

.. NOTE::
    Aquellas *Farmacias* que cumplan las siguientes condiciones **NO** podrán ser eliminadas:

        - Esten asociadas a un Pedido de Farmacia que aún no ha sido completamente enviado.

    El sistema se encargará de informar al usuario las razones por las cuales la *Farmacia* seleccionado no puede eliminarse. En dicho caso, el sistema mostrara una ventana emergente (modal) como esta:
    
    .. image:: _static/fallaeliminarfarm.png
       :align: center

.. _formulario-busqueda-farmacia:

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar sólo aquellas *Farmacias* que cumplan con algunos criterios en específico, deberá utilizar el formulario de búsqueda.

.. image:: _static/busquedafarm.png
   :align: center

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar las *Farmacias* por razon social.
    - Búsqueda avanzada: permite buscar las *Farmacias* por razon social, localidad.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todas las *Farmacias*.

El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Buscar``. El sistema visualizará aquellas *Farmacias* que cumplan con todas las condiciones especificadas.

Si el usuario desea limpiar los filtros activos, deberá presionar el boton ``Limpiar``.

.. image:: _static/limpiarfarm.png
   :align: center