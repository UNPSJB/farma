$(document).ready(
	function() {
					$('#monodrogaForm')
					.formValidation({
						
						framework: 'bootstrap',
						icon: {
							valid: 'glyphicon glyphicon-ok',
							invalid: 'glyphicon glyphicon-remove',
							validating: 'glyphicon glyphicon-refresh'
						},	
						
						excluded: ':disabled',
						fields: {
							
							monodroga: {
								validators: {
									
									notEmpty: {
										message: 'La Monodroga es Requerida'
									}
									
								}
							},
							dosis: {
								validators: {
									notEmpty: {
										message: 'La dosis es Requerida'
									}
									
								}
							},
							umedida: {
								validators: {
									notEmpty: {
										message: 'La unidad de medida es Requerida'
									}
									
								}
								
							},
						}
					})
					// Using Bootbox for color and monodroga select elements
					.find('[name="monodroga"],[name="dosis"],[name="umedida"]')
					.combobox()
					.end()

					$('#presentacionForm')
					.formValidation({
						framework: 'bootstrap',
						icon: {
							valid: 'glyphicon glyphicon-ok',
							invalid: 'glyphicon glyphicon-remove',
							validating: 'glyphicon glyphicon-refresh'
						},	
																
						excluded: ':disabled',
						fields: {
							
							descripcion: {
								validators: {
									notEmpty: {
										message: 'La descripcion es requerida'
									}
								}
							},
							cantidad: {
								validators: {
									notEmpty: {
										message: 'La cantidad es requerida'
									}
								}
							},
							umedidap: {
								validators: {
									notEmpty: {
										message: 'La unidad de medida es Requerida'
									}
								}
							},	
						}
					})
					// Using Bootbox for color and monodroga select elements
					.find('[name="descripcion"],[name="cantidad"],[name="umedidap"]')
					.combobox()
					.end()
					
					$('#nombreFform')
					.formValidation({
						
						framework: 'bootstrap',
						icon: {
							valid: 'glyphicon glyphicon-ok',
							invalid: 'glyphicon glyphicon-remove',
							validating: 'glyphicon glyphicon-refresh'
						},	
							
						excluded: ':disabled',
						fields: {
							
							nombreF: {
								validators: {
									notEmpty: {
										message: 'El nombre es Requerida'
									},
									stringLength: {
														min: 2,
														max: 50,
														message: 'The descripcion must be more than 50 and less than 1000 characters'
													}
								}
							},
							
						}
					})
					// Using Bootbox for color and monodroga select elements
					.find('[name="nombreF"]')
					.combobox()
					.end()
											
				}
);