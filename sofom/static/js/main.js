// Función para agregar filas a las tablas de referencias
document.addEventListener("DOMContentLoaded", function () {
    function setupTable(addButtonId, tableId, inputDataIds, hiddenInputId) {
        const addButton = document.getElementById(addButtonId);
        const refTableBody = document.querySelector(`#${tableId} tbody`);
        const dataInput = document.getElementById(hiddenInputId);

        if (!addButton || !refTableBody || !dataInput) {
            console.warn(`Uno o más elementos no se encontraron para ${addButtonId}, ${tableId}, ${hiddenInputId}`);
            return;
        }

        // Agregar fila a la tabla
        addButton.addEventListener("click", function () {
            const inputValues = inputDataIds.map(id => {
                const element = document.querySelector(`#${id}`);
                if (!element) {
                    console.error(`Elemento con ID ${id} no encontrado.`);
                    return null; // Devuelve null si el elemento no existe
                }
                return element.value.trim(); // Elimina espacios en blanco
            });

            if (inputValues.some(value => value === null || value === "")) {
                Swal.fire({
                    title: "Faltan campos por llenar",
                    text: "Por favor llena todos los campos antes de agregar",
                    icon: "warning"
                });
                return;
            }

            const newRow = document.createElement("tr");
            newRow.innerHTML = inputValues.map(value => `<td>${value}</td>`).join('') +
                '<td><button class="btn btn-danger btn-sm remove-row">Eliminar</button></td>';
            refTableBody.appendChild(newRow);

            // Limpia los valores de los inputs después de agregar la fila
            inputDataIds.forEach(id => {
                const element = document.querySelector(`#${id}`);
                if (element) element.value = "";
            });

            // Agregar evento para eliminar filas
            newRow.querySelector(".remove-row").addEventListener("click", function () {
                this.closest("tr").remove();
                updateHiddenField();
            });

            // Actualizar el campo oculto después de agregar una fila
            updateHiddenField();
        });

        // Función para actualizar el campo oculto con los datos de la tabla
        function updateHiddenField() {
            let data = [];
            refTableBody.querySelectorAll("tr").forEach(function (row) {
                const columns = row.querySelectorAll("td");
                const rowData = inputDataIds.reduce((acc, id, index) => {
                    acc[id] = columns[index]?.innerText || ""; // Maneja valores inexistentes
                    return acc;
                }, {});
                data.push(rowData);
            });
            dataInput.value = JSON.stringify(data);
            console.log(`Actualizado ${hiddenInputId}:`, dataInput.value); // Depuración
        }

        // Convertir los datos de la tabla en JSON antes de enviar el formulario
        const form = document.querySelector("form");
        form.addEventListener("submit", function (e) {
            e.preventDefault();

            // Asegúrate de que el campo oculto está actualizado antes de enviar
            updateHiddenField();

            // Desactiva los inputs después de actualizar
            inputDataIds.forEach(id => {
                const element = document.querySelector(`#${id}`);
                if (element) element.disabled = true;
            });

            console.log("Enviando formulario con:", dataInput.value); // Depuración
            form.submit();
        });
    }

    // Configuración de las tablas con sus respectivos IDs
    setupTable("add-ref-1", "ref-table-1", [
        "id_ref_bancos-banco",
        "id_ref_bancos-cuenta_banco",
        "id_ref_bancos-clabe_interbancaria",
        "id_ref_bancos-rfc",
        "id_ref_bancos-no_tarjeta"
    ], "bancos-data");

    setupTable("add-ref-2", "ref-table-2", [
        "id_ref_personal-nombre",
        "id_ref_personal-direccion",
        "id_ref_personal-relacion",
        "id_ref_personal-telefono"
    ], "referencias-data");

    setupTable("add-ref-3", "ref-table-3", [
        "id_ref_bancaria-institucion",
        "id_ref_bancaria-direccion_institucion",
        "id_ref_bancaria-no_cuenta",
        "id_ref_bancaria-tipo_cuenta",
        "id_ref_bancaria-telefono_institucion",
        "id_ref_bancaria-tipo_ref"
    ], "bancarias-data");

    setupTable("add-ref-4", "ref-table-4", [
        "id_contactos-apellido_paterno",
        "id_contactos-apellido_materno",
        "id_contactos-nombres",
        "id_contactos-puesto",
        "id_contactos-email",
        "id_contactos-telefono"
    ], "contactos-data");
});


// Actualizar opciones de "Número de Períodos"
document.addEventListener('DOMContentLoaded', function () {
    const periodoPagoSelect = document.getElementById('id_credi-periodo_pago');
    const numeroPeriodosSelect = document.getElementById('id_credi-numero_periodos');
    numeroPeriodosSelect.parentElement.style.display = 'none';

    function actualizarNumeroPeriodos() {
        const periodoSeleccionado = periodoPagoSelect.value;
        numeroPeriodosSelect.innerHTML = '';

        if (['QUINCENAL', 'MENSUAL', 'SEMANAL'].includes(periodoSeleccionado)) {
            numeroPeriodosSelect.parentElement.style.display = 'block';
            const SEMANAS = Array.from({ length: 57 }, (_, i) => [i + 4, `${i + 4} SEMANA(S)`]);
            const opciones = (periodoSeleccionado === 'QUINCENAL') ? QUINCENAS :
                (periodoSeleccionado === 'MENSUAL') ? MESES : SEMANAS;

            opciones.forEach(opcion => {
                const optionElement = document.createElement('option');
                optionElement.value = opcion[0];
                optionElement.textContent = opcion[1];
                numeroPeriodosSelect.appendChild(optionElement);
            });
        } else {
            numeroPeriodosSelect.parentElement.style.display = 'none';
        }
    }

    periodoPagoSelect.addEventListener('change', actualizarNumeroPeriodos);
    actualizarNumeroPeriodos();
});



// Generar PDF
function generatePDF() {
    const table = document.getElementById("amortizationTable");
    const rows = table.querySelectorAll("tbody tr");
    const data = Array.from(rows).map(row => Array.from(row.querySelectorAll("td")).map(td => td.innerText));

    fetch('/generate_pdf/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ tableData: data })
    })
        .then(response => response.ok ? response.blob() : Promise.reject('Error al generar el PDF'))
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'amortization_table.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(console.error);
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

