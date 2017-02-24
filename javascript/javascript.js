var fill_tabla = function(con) {
	var encontrada_func = JSON.parse(encontrada[con]);
	var rexi_func = JSON.parse(rexi[con]);
	var comparacion_func = JSON.parse(verification[con]);
	for (e in rexi_func) {
		if (e == "id" || e=="name" || e=="bankName" || e=="marca") {
			$("#"+e+"Rexi").text(rexi_func[e]).css("color","gray").css("font-weight","bold");
		}
		else {
			if (rexi_func[e] === true) {
				$("#"+e+"Rexi").text("Verdadero");
			} else {
				if (rexi_func[e] === false){
					if (rexi_func[e] === 0) {
						$("#"+e+"Rexi").text("0")
					}
					else {
						$("#"+e+"Rexi").text("Falso");
					}
					
				}
				else {
					$("#"+e+"Rexi").text(rexi_func[e]);
				}
			}
		}
		
	}

	/*Hasta aqui*/

	/*-------------------------------------------*/

	/*Informacion encontrada*/

	for (e in encontrada_func) {
		if (encontrada_func[e] === true) {
			$("#"+e+"Publica").text("Verdadero");
		} else {
			if (encontrada_func[e] === false){
				if (encontrada_func[e] === 0) {
					$("#"+e+"Publica").text("0")
				}
				else {
					$("#"+e+"Publica").text("Falso");
				}
				
			}
			else {
				$("#"+e+"Publica").text(encontrada_func[e]);
			}
		}
	}

	/*Verificacion*/
	for (e in comparacion_func) {
		if (comparacion_func[e]=="OK") {
			$("#"+e+"Status").text(comparacion_func[e]).css("color","green").css("font-weight","bold");
		}
		else{
			if (comparacion_func[e]=="No encontrado") {
				$("#"+e+"Status").text(comparacion_func[e]).css("color","#FE9A2E").css("font-weight","bold")
			} else {
				if (comparacion_func[e]=="No aplica") {
					$("#"+e+"Status").text(comparacion_func[e]).css("color","#0174DF").css("font-weight","bold")
				}
				else {
					if (comparacion_func[e] == "No registrado") {
						$("#"+e+"Status").text(comparacion_func[e]).css("color","purple").css("font-weight","bold")
					} else {
						$("#"+e+"Status").text(comparacion_func[e]).css("color","red").css("font-weight","bold")
					}
				}
			}
		}
		
	}
}


function presentar_Comparacion() {
	fill_tabla(0)
	$("body").prepend("<div id='header'></div>")
	for (e in verification) {
		$("#header").append("<button class='tabs' id='verification"+e+"'>"+JSON.parse(rexi[e])["name"]+"</button>");
	}
	for(let i = 0; i < verification.length; i++) {
		$('#verification' + i).click( function(){
			$(".tabs").css("background", "rgb(66, 184, 221)");
			$("#verification"+i).css("background","rgb(30,144,255)");

	    	fill_tabla(i)
	  });
	}

}

function ordenar(info) {
	var info = info
	var orden = [];
	var usa_estos = [
        "ingreso_minimo",
        "facturacion",
        "dias_de_vencimiento",
        "tasa_de_interes_en_rd",
        "tasa_de_interes_en_us",
        "cargo_por_emision",
        "renovacion_anual",
        "seguro_robo_o_perdida",
        "cargo_por_sobregiro",
        "cargo_por_mora",
        "avance_de_efectivo",
        "plan_de_lealtad",
        "recompensa",
        "bono_unidades_de_emision",
        "comercios_que_generan_unidades_extra",
        "minimo_unidades_para_canje",
        "vencimiento_de_unidades",
        "pago_de_membresia",
        "descuento_en_comercios_especificos",
        "alcance_del_descuento",
        "descuento_maximo_en_comercios",
        "descuentos_por_tipo_de_comercio",
        "catalogo_de_descuentos_ocasionales",
        "credito_diferido",
        "utiliza_tarjeta_separada",
        "establecimientos_permitidos",
        "monto_minimo_de_compra",
        "cantidad_de_cuotas_permitidas",
        "adelanto_efectivo_emergencia",
        "enfoque_empresas",
        "minimo_de_cuotas_permitidas",
        "tasa_de_interes_del_credito_diferido",
        "linea_aerea_vinculada",
        "priority_pass",
        "before_boarding",
        "servicios_de_asistencia_de_viajes",
        "servicios_de_asistencia_personal",
        "seguro_en_accidentes_de_viaje",
        "seguro_en_accidentes_en_destino_de_viaje",
        "seguro_de_autos_alquilados",
        "seguro_contra_demora_de_equipaje",
        "seguro_contra_perdida_de_equipaje",
        "seguro_contra_demora_de_viaje",
        "seguro_contra_cancelacion_de_viaje",
        "seguro_contra_perdida_de_conexion",
        "emergencia_medica_internacional",
        "proteccion_de_compras",
        "proteccion_de_precios",
        "permite_garantia",
        "programa_recuperacion_de_credito",
        "programa_educacion_financiera",
        "programa_iniciar_credito",
        "servicio_de_asistencia_a_negocios",
        "institucion_o_empresa",
        "beneficio_valor_agregado",
        "destinada_combustible",
        "porcentaje_sobre_limite"
	];
	for (e in usa_estos) {
		orden.push("<div style='color:green'>*"+usa_estos[e]+": " + "<br></div>" + info[usa_estos[e]])
	}
	return orden;
}
function setInnerHTML(element, content) {
	element.innerHTML = content;
	return element;
} 

