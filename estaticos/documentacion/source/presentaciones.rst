Presentaciones
==============
Se presentará una pantalla que contendrá un listado con todas las *Presentaciones* que se encuentren registradas en el sistema hasta la fecha. 

.. image:: _static/presentaciones.png
   :align: center

Junto con el listado, se ofrecerán un conjunto de funcionalidades que permitirán manipular estas *Presentaciones*


Estas funcionalidades son:

    - :ref:`Alta Presetación <alta-presentacion>`
    - :ref:`Modificar Presetación <modificar-presentacion>`
    - :ref:`Eliminar Presetación <eliminar-presentacion>`
    - :ref:`Formulario de Búsqueda <formulario-busqueda-presentacion>`


.. _alta-presentacion:

Alta Presentación
-----------------
Si el usuario desea crear una nueva *Presentación*, deberá presionar el botón ``Alta``. 

.. image:: _static/btnaltapres.png
   :align: center

A continuación el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/altapres.png
   :align: center

En esta parte el usuario se le presentará un formulario y deberá ingresar los datos solicitados para dar de alta una nueva *Presentación*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos vacios.
        - La cantidad ingresada no posee el formato correcto.
        - La cantidad ingresada es menor a cero.

 
Una vez completado el formulario, el usuario tendrá dos opciones: 
    
    - Presionar el botón ``Guardar y Volver``.
    - Presionar el botón ``Guardar y Continuar``.

El botón ``Guardar y Volver`` permite guardar la *Presentación* en el sistema y volver a la pantalla 
principal de *Presentaciones*.

El botón ``Guardar y Continuar`` permite guardar la *Presentación* en el sistema y seguir dando de alta nuevas *Presentaciones*.

.. _modificar-presentacion:

Modificar Presentación
----------------------
Si el usuario desea modificar los datos de una *Presentación*, deberá seleccionar el botón de **Acción** asociado a la *Presentación* y presionar la pestaña ``Modificar``.

.. image:: _static/btnmodificarpres.png
   :align: center

Una vez realizado el paso anterior, el sistema lo redirigirá a la siguiente pantalla:

.. image:: _static/modificarpres.png
   :align: center

En esta parte al usuario se le presentará un formulario y deberá actualizar los datos asociados a la *Presentación*.

.. ATTENTION::
    El sistema siempre validará que la información ingresada sea correcta. En caso de que los datos ingresados sean incorrectos el sistema lo informará. 
    En este punto, las posibles causas de errores son:

        - Uno o más campos vacios.
        - La cantidad ingresada no posee el formato correcto.
        - La cantidad ingresada es menor a cero.

Una vez completado el formulario, el usuario deberá presionar el botón ``Guardar Cambios`` y el sistema se encargara de actualizar los datos de la *Presentación* seleccionada.

.. _eliminar-presentacion:

Eliminar Presentación
---------------------
Si el usuario desea eliminar una *Presentación*, deberá seleccionar el botón de **Acción** asociado a la *Presentación* y presionar la pestaña ``Eliminar``.

.. image:: _static/btneliminarpres.png
   :align: center

Una vez realizado el paso anterior aparecerá la siguiente ventana emergente (modal):

.. image:: _static/eliminarpres.png
   :align: center

En esta parte el usuario deberá decidir si confirma la eliminación de la *Presentación* o no. Si desea confirmar la eliminación deberá presionar el botón ``Confirmar``, caso contrario, presionará el botón ``Cancelar``.

.. NOTE::
    Aquellas *Presentaciones* que cumplan las siguientes condiciones **NO** podrán ser eliminadas:

        - Esten asociadas a un medicamento.

    El sistema se encargará de informar al usuario las razones por las cuales la *Presentación* seleccionada no puede eliminarse. En dicho caso, el sistema mostrara una ventana emergente (modal) como esta:
    
    .. image:: _static/fallaeliminarpres.png
       :align: center

.. _formulario-busqueda-presentacion:

Formulario de Búsqueda
----------------------
Si el usuario desea visualizar sólo aquellas *Presentaciones* que cumplan con algunos criterios en específico, deberá utilizar el formulario de búsqueda.

.. image:: _static/busquedapres.png
   :align: center

Este formulario sólo cuenta con la opción de búsqueda simple en base a la descripción de la *Presentación*. 

.. NOTE::
    Este campo es opcional, de no especificarse ningún criterio de búsqueda el sistema mostrará todas las *Presentaciones*.

El usuario tendrá que ingresar los parámetros de búsqueda en el formulario, y presionar el botón ``Buscar``. El sistema visualizará aquellas *Presentaciones* que cumplan con todas las condiciones especificadas.