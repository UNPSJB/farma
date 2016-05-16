Clínicas
========
Se presentará una pantalla que contendrá un listado con todas las *Clínicas* que se encuentren registradas en el sistema hasta la fecha. 

.. image:: _static/clinicas.png
   :align: center

Junto con el listado, se presentarán un conjunto de funcionalidades que permitirán manipular estas *Clínicas*.

Estas funcionalidades son:

    - :ref:`Alta Clínica <alta-clinica>`
    - :ref:`Ver Obras Sociales <ver-obras-sociales>`
    - :ref:`Modificar Clínica <modificar-clinica>`
    - :ref:`Eliminar Clínica <eliminar-clinica>`
    - :ref:`Formulario de Búsqueda <formulario-busqueda-clinica>`
    
.. _alta-clinica:

Alta Clínica
------------
Si el usuario desea crear una nueva *Clínica*, deberá presionar el botón ``Alta``. 

.. image:: _static/btnaltaclin.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/altaclin.png
   :align: center

En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Clínica*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos obligatorios vacíos.
        - Uno o más campos con un formato incorrecto.
        - El CUIT ingresado ya se encuentra asociado a otra organización.
     
Una vez completado el formulario, el usuario tendrá dos opciones: 
    
    - Presionar el botón ``Guardar y Volver``.
    - Presionar el botón ``Guardar y Continuar``.

El botón ``Guardar y Volver`` permite guardar la *Clínica* en el sistema y volver a la pantalla 
principal de *Clínicas*..

El botón ``Guardar y Continuar`` permite guardar la *Clínica* en el sistema y seguir dando de alta nuevas *Clínicas*.

.. _ver-obras-sociales:

Ver Obras Sociales
------------------
Si el usuario desea ver las obras sociales asociadas a una *Clínica*, deberá seleccionar el botón de **Acción** asociado a la *Clínica* y presionar la pestaña ``Ver Obras Sociales``.

.. image:: _static/btnobrasclin.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/obrasclin.png
   :align: center

Esta ventana mostrará todas los obras sociales vinculadas a la *Clínica* seleccionada.
   
.. _modificar-clinica:

Modificar Clínica
-----------------
Si el usuario desea modificar los datos de una *Clínica*, deberá seleccionar el botón de **Acción** asociado a la *Clínica* y presionar la pestaña ``Modificar``.

.. image:: _static/btnmodificarclin.png
   :align: center

Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/modificarclin.png
   :align: center

En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Clínica*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos obligatorios vacíos.
        - Uno o más campos con un formato incorrecto.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar Cambios`` y el sistema se encargara de actualizar los datos de la *Clínica* seleccionada.

.. _eliminar-clinica:

Eliminar Clínica
----------------
Si el usuario desea eliminar una *Clínica*, deberá seleccionar el botón de **Acción** asociado a la *Clínica* y presionar la pestaña ``Eliminar``.

.. image:: _static/btneliminarclin.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/eliminarclin.png
   :align: center

En esta parte el usuario deberá decidir si confirma la eliminación de la *Clínica* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.

.. _formulario-busqueda-clinica:

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar sólo aquellas *Clínicas* que cumplan con algunos criterios en específico, deberá utilizar el formulario de búsqueda.

.. image:: _static/busquedaclin.png
   :align: center

Este formulario cuenta con dos modalidades:

    - Búsqueda simple: permite buscar las *Clínicas* por razon social.
    - Búsqueda avanzada: permite buscar las *Clínicas* por razon social, localidad, obra social.

.. NOTE::
    Todos los campos son opcionales, de no especificarse ningún criterio de búsqueda el sistema mostrará todas las *Clínicas*.

El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Buscar``. El sistema visualizará aquellas *Clínicas* que cumplan con todas las condiciones especificadas.

Si el usuario desea limpiar los filtros activos, deberá presionar el boton ``Limpiar``.

.. image:: _static/limpiarclin.png
   :align: center