$(document).ready(function() {

	    //registrar pedido
	    $("#registrar-pedido").click(function(event) {
	        $("#inputLaboratorio").prop('disabled', false);
	        var btn = $("#boton-abm");
	        if (btn.hasClass("btn-warning"))
	            btn.removeClass("btn-warning");
	        else {
	            if (btn.hasClass("btn-danger"))
	                btn.removeClass("btn-danger");
	        }
	        if (!btn.hasClass("btn-success")) {
	            btn.addClass("btn-success");
	            btn.text("Registrar");
	            $(".panel-title span").text("[Registrar]");
	            if ($("#botones-detalles").hasClass("hidden"))
	                $("#botones-detalles").removeClass("hidden");
	            if(! $("#btn-editar").hasClass("hidden"))
	            	$("#btn-editar").addClass("hidden");
	        }
	    });

	    //modificar pedido
	    $("#modificar-pedido").click(function(event) {
	        $("#inputLaboratorio").prop('disabled', true);
	        var btn = $("#boton-abm");
	        if (btn.hasClass("btn-success"))
	            btn.removeClass("btn-success");
	        else {
	            if (btn.hasClass("btn-danger"))
	                btn.removeClass("btn-danger");
	        }
	        if (!btn.hasClass("btn-warning")) {
	            btn.addClass("btn-warning");
	            btn.text("Guardar Cambios");
	            $(".panel-title span").text("[Modificar]");
	            if ($("#botones-detalles").hasClass("hidden"))
	                $("#botones-detalles").removeClass("hidden");
	            if($("#btn-editar").hasClass("hidden"))
	            	$("#btn-editar").removeClass("hidden");
	        }
	    });

	    //eliminar pedido
	    $("#eliminar-pedido").click(function(event) {
	        $("#inputLaboratorio").prop('disabled', true);
	        var btn = $("#boton-abm");
	        if (btn.hasClass("btn-success"))
	            btn.removeClass("btn-success");
	        else {
	            if (btn.hasClass("btn-warning"))
	                btn.removeClass("btn-warning");
	        }
	        if (!btn.hasClass("btn-danger")) {
	            btn.addClass("btn-danger");
	            btn.text("Eliminar");
	            $(".panel-title span").text("[Eliminar]");
	            $("#botones-detalles").addClass("hidden"); 
	        }
	    });
});