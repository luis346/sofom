document.addEventListener('DOMContentLoaded', function () {
    let solicitudes = [];
    let clientesAlta = [];
    let clientesValidacion = [];
    let creditoAutorizado = [];

    try {
        solicitudes = JSON.parse(document.getElementById('clientesData').textContent);
        clientesValidacion = JSON.parse(document.getElementById('clientesDataValidacion').textContent);
        creditoAutorizado = JSON.parse(document.getElementById('clientesDataAutorizado').textContent);
        console.log('Clientes JSON:', document.getElementById('clientesData').textContent);
        console.log('Datos de solicitudes:', solicitudes);

        solicitudes.forEach((solicitud) => {
            const estado = solicitud.status?.trim().toLowerCase();
            console.log('Estado de solicitud:', estado); 
            if (estado === 'alta') {
                clientesAlta.push(solicitud);
            } else if (estado === 'validacion') {
                clientesValidacion.push(solicitud);
            } else if (estado === 'aprobado') {
                creditoAutorizado.push(solicitud);
            }
        });
        console.log("Clientes clasificados: Alta:", clientesAlta, "Validación:", clientesValidacion, "Crédito:", creditoAutorizado);
    } catch (error) {
        console.error("Error al analizar JSON de clientesData:", error);
    }

    const tableBody = document.querySelector('#clientesTable tbody');
    const pdfButton = document.querySelector('button[onclick="generatePDF()"]');
    const modal = new bootstrap.Modal(document.getElementById('miModal'), {});
   // Tu código para cargar y mostrar el modal
    const modalPLD = new bootstrap.Modal(document.getElementById('modalPLD'));
    const modalCredito = new bootstrap.Modal(document.getElementById('modalCredito'));
    const formSolicitud = document.getElementById('formSolicitud');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function populateTable(solicitudes) {
        console.log('Solicitudes recibidas para mostrar en la tabla:', solicitudes); 
    
        tableBody.innerHTML = ''; 
        if (solicitudes.length > 0) {
            solicitudes.forEach(solicitud => {
                const row = `<tr data-id="${solicitud.id}">
                                <td>${solicitud.id}</td>
                                <td>${solicitud.apellido_paterno}</td>
                                <td>${solicitud.apellido_materno}</td>
                                <td>${solicitud.nombres}</td>
                            </tr>`;
                tableBody.insertAdjacentHTML('beforeend', row);
            });
            pdfButton.disabled = false; 
        } else {
            const row = `<tr><td colspan="4">No se encontraron clientes.</td></tr>`;
            tableBody.insertAdjacentHTML('beforeend', row);
            pdfButton.disabled = true; 
        }
    }

    function cargarDatosFormulario(cliente) {
        console.log('Cliente cargado en el formulario:', cliente);

        const campos = [
            'apellido_paterno', 'apellido_materno', 'nombres', 'fecha_nacimiento', 'edad',
            'rfc', 'genero', 'estado_civil', 'dependientes', 'tipo_id_oficial',
            'clave_id_oficial', 'curp', 'nacionalidad', 'pais_nacimiento',
            'entidad_federativa_nacimiento', 'proveedor_recursos', 'mercado', 'imss',
            'codigo_postal', 'estado', 'municipio', 'colonia', 'calle',
            'no_exterior', 'no_interior', 'entre_calles', 'tipo_vivienda',
            'anios_residencia', 'telefono_fijo', 'celular', 'telefono_avisos', 'email'
        ];

        campos.forEach(campo => {
            const input = document.getElementById(`id_solicitud-${campo}`);
            if (input) {
                input.value = cliente[campo] !== undefined ? cliente[campo] : '';
            } else {
                console.log(`No se encontró el campo con ID: id_solicitud-${campo}`);
            }
        });

        // Actualizar el valor del input oculto con el id de la solicitud
        const solicitudIdInput = document.querySelector('[name="solicitud_id"]');
        if (solicitudIdInput) {
            solicitudIdInput.value = cliente.id;
        }
        modal.show(); 
    }
// Función para cargar datos en el formulario del modal
function cargarDatosFormularioPLD(cliente) {
    console.log('Cliente cargado en el formulario PLD:', cliente);

    const camposPLD = [
        'nombres', 'rfc', 'curp', 'fecha_nacimiento', 'pais_nacimiento'
    ];

    camposPLD.forEach(campo => {
        const input = document.getElementById(`id_pld-${campo}`);
        if (input) {
            input.value = cliente[campo] !== undefined ? cliente[campo] : '';
        } else {
            console.log(`No se encontró el campo PLD con ID: id_pld-${campo}`);
        }
    });

    const solicitudIdInput = document.querySelector('[name="solicitud_id_pld"]');
    if (solicitudIdInput) {
        solicitudIdInput.value = cliente.id;
    }

    modalPLD.show();
}
document.getElementById('validarPLD').addEventListener('click', async function () {
    const solicitudId = document.getElementById('solicitud_id_pld').value; // Asegúrate de que este ID corresponda al campo que contiene el ID de la solicitud.

    try {
        const response = await fetch('http://127.0.0.1:8000/crear-credito/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'), // Asegúrate de enviar el CSRF token para las solicitudes POST.
            },
            body: new URLSearchParams({
                'validate_pld': 'true',
                'solicitud_id_pld': solicitudId
            }),
        });

        if (!response.ok) {
            throw new Error(`Error ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();

        if (data.status === 'rechazado') {
            let message = data.message;

            // Mostrar coincidencias locales
            let coincidenciasLocales = data.coincidencias_local.length > 0 ? data.coincidencias_local.join(', ') : 'Ninguna';

            // Mostrar coincidencias SDN con puntajes
            let coincidenciasSDN = data.coincidencias_sdn.length > 0 
                ? data.coincidencias_sdn.map(item => `${item} (Score: 100)`).join(', ')  // Suponiendo que las coincidencias son solo nombres, sin necesidad de objetos adicionales
                : 'Ninguna';

            Swal.fire({
                icon: 'error',
                title: 'Cliente rechazado',
                text: message,
                footer: `Coincidencias locales: ${coincidenciasLocales}<br>
                         Coincidencias SDN: ${coincidenciasSDN}`
            }).then(() => {
                // Cerrar el modal y recargar la página
                window.location.reload();  // Recarga la página
            });
        } else if (data.status === 'aprobado') {
            Swal.fire({
                icon: 'success',
                title: 'Cliente aprobado',
                text: data.message,
            }).then(() => {
                // Cerrar el modal y recargar la página
                window.location.reload();  // Recarga la página
            });
        } else {
            Swal.fire({
                icon: 'warning',
                title: 'Validación incompleta',
                text: data.message,
            });
        }
    } catch (error) {
        console.error('Error en la validación PLD:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Hubo un problema al validar el cliente.',
        });
    }
});

//Funcion para cargar modalCredito 
function cargarDatosModalCredito(cliente){
    const solicitudIdInput = document.querySelector('[name="solicitud_id_credito"]');
    if (solicitudIdInput) {
        solicitudIdInput.value = cliente.id;
    }

    modalCredito.show();
}

// Función para obtener el CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

    function cargarDatosSolicitud(solicitudId) {
        console.log('ID de solicitud recibido:', solicitudId);
        const cliente = solicitudes.find(c => c.id == solicitudId);
        console.log('Cliente encontrado:', cliente);

        if (cliente) {
            cargarDatosFormulario(cliente);
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudo encontrar el cliente',
                confirmButtonText: 'OK'
            });
        }
    }

    function cargarDatosSolicitudValidacion(solicitudId) {
        console.log('ID de solicitud recibido:', solicitudId);
        const cliente = clientesValidacion.find(c => c.id == solicitudId);
        console.log('Cliente encontrado:', cliente);

        if (cliente) {
            cargarDatosFormularioPLD(cliente); // Mostrar modal de PLD
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudo encontrar el cliente',
                confirmButtonText: 'OK'
            });
        }
    }

    function cargarDatosSolicitudAutorizada(solicitudId) {
        console.log('ID de solicitud recibido:', solicitudId);
        const cliente = creditoAutorizado.find(c => c.id == solicitudId);
        console.log('Cliente encontrado:', cliente);

        if (cliente) {
            cargarDatosFormulario(cliente); // Mostrar modal de PLD
        } else {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudo encontrar el cliente',
                confirmButtonText: 'OK'
            });
        }
    }

    tableBody.addEventListener('click', function (e) {
        if (e.target.tagName === 'TD') {
            let solicitudId = parseInt(e.target.parentElement.getAttribute('data-id'), 10);
            
            // Buscar en ambos arrays, Alta y Validación
            const clienteAlta = clientesAlta.find(c => c.id == solicitudId);
            const clienteValidacion = clientesValidacion.find(c => c.id == solicitudId);
            const clienteAutorizado = creditoAutorizado.find(c => c.id == solicitudId);
         
    
            if (clienteAlta) {
                cargarDatosFormulario(clienteAlta); // Cargar datos de "alta"
            } else if (clienteValidacion) {
                cargarDatosFormularioPLD(clienteValidacion); // Cargar datos de "validación" y mostrar modal PLD  
            } else if (clienteAutorizado) {
                cargarDatosModalCredito(clienteAutorizado);    
            } else {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'No se pudo encontrar el cliente',
                    confirmButtonText: 'OK'
                });
            }
        }
    });
    formSolicitud.addEventListener('submit', function (e) {
        e.preventDefault();
        Swal.fire({
            icon: 'success',
            title: 'Datos actualizados',
            text: 'Los datos de la solicitud se han actualizado correctamente',
            confirmButtonText: 'OK'
        }).then(() => {
            const solicitudId = formSolicitud.querySelector('[name="solicitud_id"]').value;
            const clienteActualizado = solicitudes.find(c => c.id == solicitudId);

            if (clienteActualizado) {
                clienteActualizado.status = 'validacion'; // Cambiar estado a 'validacion'

                clientesAlta = clientesAlta.filter(c => c.id != clienteActualizado.id);
                clientesValidacion.push(clienteActualizado);

                populateTable(clientesValidacion);
            }
            formSolicitud.submit();
        });
    });
    
    document.querySelector('#clientes-alta').addEventListener('change', function () {
        const filtro = this.value;
    
        console.log("Filtro seleccionado:", filtro);
    
        if (filtro === 'alta') {
            console.log("Datos clientesAlta:", clientesAlta);
            populateTable(clientesAlta);
        } else if (filtro === 'validacion') {
            console.log("Datos clientesValidacion:", clientesValidacion);
            populateTable(clientesValidacion);
        } else if (filtro === 'aprobado') {
            console.log("Datos creditoAutorizado:", creditoAutorizado);
            populateTable(creditoAutorizado);
        } else {
            const tableBody = document.querySelector('#clientesTable tbody');
            tableBody.innerHTML = `<tr><td colspan="4">Seleccione una opción para ver los clientes.</td></tr>`;
        }
    });
    
    tableBody.innerHTML = `<tr><td colspan="4">Seleccione una opción para ver los clientes.</td></tr>`;
    pdfButton.disabled = true; 
});


// Generar PDF de Tabla de Amortización y Contrato
function generatePDF() {
    const table = document.getElementById("amortizationTable");
    const rows = table.querySelectorAll("tbody tr");
    const data = Array.from(rows).map(row =>
        Array.from(row.querySelectorAll("td")).map(td => td.innerText)
    );

    // Generar Tabla de Amortización
    fetch('/generate_pdf/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ tableData: data })
    })
    .then(response => response.ok ? response.blob() : Promise.reject('Error al generar el PDF de amortización'))
    .then(blob => downloadPDF(blob, 'tabla_amortizacion.pdf')) // Descargar el PDF de amortización
    .then(() => {
        // Generar Contrato
        return fetch('/generate_contract_pdf/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
    })
    .then(response => response.ok ? response.blob() : Promise.reject('Error al generar el PDF del contrato'))
    .then(blob => downloadPDF(blob, 'contrato_credito.pdf')) // Descargar el PDF del contrato
    .catch(console.error);
}

// Función auxiliar para descargar PDFs
function downloadPDF(blob, filename) {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.style.display = 'none';
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
}



// Obtener el token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        document.cookie.split(';').some(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                return true;
            }
        });
    }
    return cookieValue;
}


//Funciones para el simulador de credito

// Función para calcular el costo del seguro según el monto del préstamo
function calcularSeguroIndividual(montoPrestamo) {
    let precioSeguro = 30.00; // Costo base de seguro
    if (montoPrestamo >= 2000 && montoPrestamo <= 4500) {
        precioSeguro = 70.00;
    } else if (montoPrestamo >= 5000 && montoPrestamo <= 6500) {
        precioSeguro = 85.00;
    } else if (montoPrestamo >= 7000 && montoPrestamo <= 10000) {
        precioSeguro = 93.00;
    } else if (montoPrestamo >= 10500 && montoPrestamo <= 15000) {
        precioSeguro = 98.00;
    } else if (montoPrestamo >= 15500 && montoPrestamo <= 25000) {
        precioSeguro = 103.00;
    }
    return precioSeguro;
}


function calcularSeguroFamiliar(montoPrestamo) {
    let precioSeguro = 60.00; //Costo base del seguro
    if (montoPrestamo >= 2000 && montoPrestamo <= 4500) {
        precioSeguro = 119.00;
    } else if (montoPrestamo >= 5000 && montoPrestamo <= 6500) {
        precioSeguro = 144.50;
    } else if (montoPrestamo >= 7000 && montoPrestamo <= 10000) {
        precioSeguro = 158.10;
    } else if (montoPrestamo >= 10500 && montoPrestamo <= 15000) {
        precioSeguro = 166.60;
    } else if (montoPrestamo >= 15500 && montoPrestamo <= 25000) {
        precioSeguro = 175.10;
    }
    return precioSeguro;
}

// Función para calcular el pago del préstamo 
function calculatePayment() {
    const loanAmountInput = document.getElementById('loanAmount');
    const loanTermInput = document.getElementById('id_loanTerm');
    const minInterestRateInput = document.getElementById('minInterestRate');
    const maxInterestRateInput = document.getElementById('maxInterestRate');
    const commissionInput = document.getElementById('commission');
    const insuranceInput = document.getElementById('insurance');
    const firstPaymentDateInput = document.getElementById('fecha_inicial');
    const lastPaymentDateInput = document.getElementById('fecha_final');
    const paymentPeriodInput = document.getElementById('id_paymentPeriod');

    if (!loanAmountInput.value || !loanTermInput.value || isNaN(minInterestRateInput.value) || isNaN(maxInterestRateInput.value) || !firstPaymentDateInput.value || !lastPaymentDateInput.value) {
        Swal.fire({
            title: "Faltan campos por llenar",
            text: "Por favor llene todos los campos",
            icon: "warning"
        });
        return;
    }

    const loanAmount = parseFloat(loanAmountInput.value);
    const loanTerm = parseInt(loanTermInput.value); // Plazo en semanas o meses
    const minInterestRate = parseFloat(minInterestRateInput.value) / 100;
    const maxInterestRate = parseFloat(maxInterestRateInput.value);
    const commissionRate = 2; // Comisión obligatoria al 2%
    const CAT = 275.91; // CAT predeterminado al 275.91%
    const firstPaymentDate = new Date(firstPaymentDateInput.value);
    const lastPaymentDate = new Date(lastPaymentDateInput.value);
    const paymentPeriod = paymentPeriodInput.value;

    // Comisión
    let totalCommission = (commissionRate / 100) * loanAmount;
    commissionInput.value = totalCommission.toFixed(2);
    // Seguro según checkbox o radios
    let insuranceAmount = 0;
    const insuranceType = document.querySelector('input[name="insuranceType"]:checked'); 

    // Obtener el costo base del seguro en función del tipo de seguro seleccionado
    let seguroIndivi = calcularSeguroIndividual(loanAmount);
    let seguroFamili = calcularSeguroFamiliar(loanAmount);

    // Definir el multiplicador según el plazo seleccionado
    let plazoMultiplicador = 0;
    if (paymentPeriod === 'MENSUAL') {
        plazoMultiplicador = loanTerm;
    } else if (paymentPeriod === 'QUINCENAL') {
        plazoMultiplicador = loanTerm / 2;
    } else if (paymentPeriod === 'SEMANAL') {
        plazoMultiplicador = loanTerm / 4;
    }

    // Selección del seguro basado en el tipo elegido
    if (insuranceType && insuranceType.value === 'individual') {
        insuranceAmount = seguroIndivi * plazoMultiplicador;
    } else if (insuranceType && insuranceType.value === 'familiar') {
        insuranceAmount = seguroFamili * plazoMultiplicador;
    }

    // Seguro según selección
    if (document.getElementById('insurance_des').checked) {
        insuranceAmount = 0;
    } else if (document.getElementById('insurance_cobra_aparte').checked) {
        insuranceAmount = (insuranceType.value === "individual") ? insuranceAmount : insuranceAmount;
    } else if (document.getElementById('insurance_financea').checked) {
        insuranceAmount = (insuranceType.value === "familiar") ? insuranceAmount: insuranceAmount;
    }

    // Cálculo de la comisión
    if (document.getElementById('commission_individual').checked) {
        totalCommission = 0;
    } else if (document.getElementById('commission_cobra_aparte').checked) {
        totalCommission = (commissionRate / 100) * loanAmount;
    } else if (document.getElementById('commission_financea').checked) {
        totalCommission = (commissionRate / 100) * loanAmount;
    }
    commissionInput.value = totalCommission.toFixed(2);

    document.getElementById('insurance_pesos').value = insuranceAmount.toFixed(2);
    insuranceInput.value = insuranceAmount.toFixed(2);

    const totalPayable = loanAmount + totalCommission + insuranceAmount;
    const paymentFrequency = (paymentPeriod === 'MENSUAL') ? 30 : (paymentPeriod === 'QUINCENAL' ? 15 : 7);
    const totalDays = Math.floor((lastPaymentDate - firstPaymentDate) / (1000 * 60 * 60 * 24));
    const numberOfPayments = Math.ceil(totalDays / paymentFrequency);

    // Cálculo de tasa de interés
    let monthlyPayment;
    const monthlyRate = minInterestRate / 12;
    if (document.getElementById('id_flat').checked) {
        monthlyPayment = (loanAmount * minInterestRate / (12 / paymentFrequency)) + (loanAmount / numberOfPayments);
    } else {
        monthlyPayment = totalPayable * monthlyRate / (1 - Math.pow(1 + monthlyRate, -numberOfPayments));
    }

    const totalInterest = (monthlyPayment * numberOfPayments) - totalPayable;
    const ivaInterest = totalInterest * 0.16;

    document.getElementById('monthlyPayment').value = monthlyPayment.toFixed(2);
    document.getElementById('numberOfPayments').value = numberOfPayments;
    document.getElementById('totalLoan').value = loanAmount.toFixed(2);
    document.getElementById('capital').value = loanAmount.toFixed(2);
    document.getElementById('interest').value = totalInterest.toFixed(2);
    document.getElementById('ivaInterest').value = ivaInterest.toFixed(2);
    document.getElementById('totalPayable').value = (totalPayable + ivaInterest).toFixed(2);
    document.getElementById('cat').value = CAT.toFixed(2);

    // Generar tabla de amortización
    const tableBody = document.querySelector('#amortizationTable tbody');
    tableBody.innerHTML = '';
    let remainingBalance = totalPayable;

    for (let i = 1; i <= numberOfPayments; i++) {
        const paymentDate = new Date(firstPaymentDate);
        paymentDate.setDate(paymentDate.getDate() + (i - 1) * paymentFrequency);

        const interestPayment = document.getElementById('id_flat').checked
            ? (loanAmount * minInterestRate / (12 / paymentFrequency))
            : remainingBalance * monthlyRate;

        const ivaInterestPayment = interestPayment * 0.16;
        const totalPayment = monthlyPayment + totalCommission + insuranceAmount;
        const capitalPayment = totalPayment - interestPayment - totalCommission - insuranceAmount;
        remainingBalance -= capitalPayment;

        const row = `
            <tr>
                <td>${i}</td>
                <td>${paymentDate.toLocaleDateString()}</td>
                <td>${ivaInterestPayment.toFixed(2)}</td>
                <td>${interestPayment.toFixed(2)}</td>
                <td>${totalCommission.toFixed(2)}</td>
                <td>${insuranceAmount.toFixed(2)}</td>
                <td>${totalPayment.toFixed(2)}</td>
                <td>${capitalPayment.toFixed(2)}</td>
                <td>${remainingBalance.toFixed(2)}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    }
}

// Constante de semanas
const SEMANAS = [];
for (let i = 4; i <= 60; i++) {
    SEMANAS.push([i, `${i} SEMANA(S)`]);
}

// $(document).ready para gestionar opciones de períodos y fechas
$(document).ready(function () {
    const periodOptions = {
        'QUINCENAL': QUINCENAS,
        'MENSUAL': MESES,
        'SEMANAL': SEMANAS
    };

    // Actualizar opciones del plazo
    $('#id_paymentPeriod').change(function () {
        const paymentPeriod = $(this).val();
        const $loanTerm = $('#id_loanTerm');
        $loanTerm.empty();

        if (periodOptions[paymentPeriod]) {
            periodOptions[paymentPeriod].forEach(function (option) {
                $loanTerm.append(`<option value="${option[0]}">${option[1]}</option>`);
            });
        }
    });

    // Calcular la fecha final basado en plazo y periodo de pago
    $('#id_loanTerm').change(function () {
        const plazo = parseInt($(this).val());
        const paymentPeriod = $('#id_paymentPeriod').val();
        const today = new Date();
        const fecha_inicial = new Date(today);
        const fecha_final = new Date(today);

        if (paymentPeriod === 'SEMANAL') {
            fecha_final.setDate(fecha_inicial.getDate() + (7 * plazo));
        } else if (paymentPeriod === 'QUINCENAL') {
            fecha_final.setDate(fecha_inicial.getDate() + (15 * plazo));
        } else if (paymentPeriod === 'MENSUAL') {
            fecha_final.setMonth(fecha_inicial.getMonth() + plazo);
        }

        $('#fecha_inicial').val(fecha_inicial.toISOString().split('T')[0]);
        $('#fecha_final').val(fecha_final.toISOString().split('T')[0]);
    });
});

// Función para actualizar tasas
function updateRates() {
    const interestRate = parseFloat(document.getElementById('interestRate').value);
    if (!isNaN(interestRate)) {
        document.getElementById('minInterestRate').value = (interestRate - 60).toFixed(2);
        document.getElementById('maxInterestRate').value = (interestRate + 60).toFixed(2);
    } else {
        document.getElementById('minInterestRate').value = '';
        document.getElementById('maxInterestRate').value = '';
    }
}
