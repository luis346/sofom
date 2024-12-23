$(document).ready(function () {
  // Evento para manejar el cambio del código postal de solicitud
$('#id_solicitud-codigo_postal').on('change', function () {
    var codigo_postal = $(this).val();
    if (codigo_postal) {
        $.ajax({
            url: obtenerDatosCpUrl, // URL de tu vista que devuelve datos de códigos postales
            data: { 'codigo_postal': codigo_postal },
            success: function (data) {
                console.log(data); // Verifica la respuesta
                if (data.error) {
                    alert(data.error);
                } else {
                    // Establecer los valores de estado y municipio
                    $('#id_solicitud-estado').val(data.estado);
                    $('#id_solicitud-municipio').val(data.municipio);

                    // Limpiar el combo box de colonias
                    $('#id_solicitud-colonia').empty();
                    $('#id_solicitud-colonia').append('<option value="">Selecciona una colonia</option>');

                  

                    // Llenar el combo box con las colonias correspondientes
                    data.colonias.forEach(function (colonia) {
                        console.log(colonia)
                        $('#id_solicitud-colonia').append('<option value="' + colonia.nombre + '">' + colonia.nombre + '</option>');
                    });
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                console.error("Error en la solicitud:", textStatus, errorThrown);
            }
        });
    } else {
        // Si no hay código postal, limpiar los campos de estado, municipio y colonias
        $('#id_solicitud-estado').val('');
        $('#id_solicitud-municipio').val('');
        $('#id_solicitud-colonia').empty();
        $('#id_solicitud-colonia').append('<option value="">Selecciona una colonia</option>');
    }
});

    // Evento para manejar el cambio del código postal de cónyuge
    $('#id_info-soli_codigo_postal').on('change', function () {
        var codigo_postal = $(this).val();
        if (codigo_postal) {
            $.ajax({
                url: obtenerDatosCpUrl, // URL de tu vista que devuelve datos de códigos postales
                data: { 'codigo_postal': codigo_postal },
                success: function (data) {
                    console.log(data); // Verifica la respuesta
                    if (data.error) {
                        alert(data.error);
                    } else {
                        // Establecer los valores de estado y municipio
                        $('#id_info-soli_estado').val(data.estado);
                        $('#id_info-soli_municipio').val(data.municipio);
    
                        // Limpiar el combo box de colonias
                        $('#id_info-soli_colonia').empty();
                        $('#id_info-soli_colonia').append('<option value="">Selecciona una colonia</option>');
    
                      
    
                        // Llenar el combo box con las colonias correspondientes
                        data.colonias.forEach(function (colonia) {
                            console.log(colonia)
                            $('#id_info-soli_colonia').append('<option value="' + colonia.nombre + '">' + colonia.nombre + '</option>');
                        });
                    }
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.error("Error en la solicitud:", textStatus, errorThrown);
                }
            });
        } else {
            // Si no hay código postal, limpiar los campos de estado, municipio y colonias
            $('#id_info-soli_municipio').val('');
            $('#id_info-soli_estado').val('');
            $('#id_info-soli_colonia').empty();
            $('#id_info-soli_colonia').append('<option value="">Selecciona una colonia</option>');
        }
    });
    
    // Calcular antigüedad del cónyuge
    const fechaIngresoInput = document.getElementById('id_conyuge-fecha_ingreso');
    const antiguedadInput = document.getElementById('id_conyuge-antiguedad');

    if (fechaIngresoInput && antiguedadInput) {
        fechaIngresoInput.addEventListener('change', function () {
            const fechaIngreso = new Date(this.value);
            const hoy = new Date();
            const diferenciaAnios = hoy.getFullYear() - fechaIngreso.getFullYear();
            const antiguedad = hoy.getDate() < fechaIngreso.getDate() ? diferenciaAnios - 1 : diferenciaAnios;
            antiguedadInput.value = `${antiguedad} años`;
        });
    }

    // Cálculo de ingreso neto
    const ingresoMensualInput = document.getElementById('id_info-ingreso_mensual');
    const descuentoInput = document.getElementById('id_info-descuento');
    const ingresoNetoInput = document.getElementById('id_info-ingreso_neto');

    function calcularIngresoNeto() {
        const ingresoMensual = parseFloat(ingresoMensualInput.value) || 0;
        const descuento = parseFloat(descuentoInput.value) || 0;
        ingresoNetoInput.value = (ingresoMensual - descuento).toFixed(2);
    }

    if (ingresoMensualInput && descuentoInput && ingresoNetoInput) {
        ingresoMensualInput.addEventListener('input', calcularIngresoNeto);
        descuentoInput.addEventListener('input', calcularIngresoNeto);
    }

});

