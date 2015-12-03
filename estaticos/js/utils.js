/*
<<Descripción: Función que sirve para seleccionar una fila de una tabla y devolver su id>>
El parámetro recibido indica la fila de la tabla a seleccionar
Obs -> Funciona en conjunto con la clase active de bootstrap
*/
function select_row_table(row){
	var t = $(row).closest("table");
	$("tr", t).removeClass("active");
	$(row).addClass("active");
	var m = $(row).data("id");
	console.log(m);
	return m;
}

/*
<<Descripción: Función que sirve para retornar el id de la fila seleccionada, de no haber ninguna 
fila seleccionada retorna null>>
*/
function get_selected_row(){
	var $row = $("tr.active");
	if($row.length){
		return $row.data("id");
	}	
	return null;
}

/*
<<Descripción: Función que oculta o muestra una lista de elementos>>
El primer parámetro es un array que contiene los elementos que van a ser mostrados u ocultados
El segundo parámetro es un booleano que indica la acción a ejecutar, true=ocultar o false= mostrar 
Obs -> Funciona en conjunto con la clase hidden de bootstrap 
*/
function ocultarElementos(targets, is_hidden){
	for(var i=0; i < targets.length; i++){
		if(is_hidden)
			agregarClase(targets, "hidden", true); //agrega clase hidden
		else
			agregarClase(targets, "hidden", false); //remueve clase hidden
	}
}

/*
<<Descripción: Función que agrega o elimina una clase a una lista de elementos>>
El primer parámetro es un array que contiene los elementos a los cuales se les va a agregar o eliminar una clase	
El segundo parámetro es el nombre de la clase que se le aplicará o removerá a los elementos indicados en el array(primer parámetro)	
El tercer parámetro indica la acción a ejecutar, true=add o false=remove
*/
function agregarClase(targets, name_class, is_add){
	for(var i=0; i < targets.length; i++){
		if(is_add)
			$(targets[i]).addClass(name_class);
		else
			$(targets[i]).removeClass(name_class);
	}
}

function crear_baja(url, id){
    if (id) {
        var urlFinal = url + id + "/";
        var $modal = $("#modal-baja");
        var $confirmar = $(".confirmar", $modal);
        $modal.modal("show");
        $confirmar.attr("href", urlFinal);
    }
}
