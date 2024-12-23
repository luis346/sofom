from django.shortcuts import render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Q
from fuzzywuzzy import process, fuzz
from django.http import JsonResponse, HttpResponse
from datetime import datetime, timedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.utils import timezone
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import SolicitudForm, SolicitudConyugeForm, InfoForm, BancosForm, ReferenciasPersonalesForm, ReferenciasBancariasForm, CreditoForm, ContactosForm, SolicitudSerializer
from .models import CodigoPostal, DatosBanco, ReferenciasPersonales, ReferenciasBancarias, Solicitud, Contactos, Sucursal, Datos_Credito, ListaNegra
import json, csv, os, xlwt


def home(request):
    # Contar clientes por estado
    clientes_estado = Solicitud.objects.values('status').annotate(total=Count('id'))

    # Contar solicitudes por día de la semana (lunes a viernes)
    start_date = datetime.now() - timedelta(days=datetime.now().weekday())  # Lunes de esta semana
    end_date = start_date + timedelta(days=4)  # Viernes de esta semana
    solicitudes_periodo = Solicitud.objects.filter(
        created_at__date__range=(start_date, end_date)
    ).extra({'day': "date(created_at)"}).values('day').annotate(total=Count('id')).order_by('day')

    # Serializar los datos para enviarlos al template
    context = {
        'clientes_estado': json.dumps(list(clientes_estado)),  # Serialización JSON
        'solicitudes_periodo': json.dumps(list(solicitudes_periodo)),  # Serialización JSON
    }
    return render(request, 'home.html', context)


def registro(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                # Usar el sistema de mensajes para mostrar una alerta de éxito
                messages.success(request, 'El usuario se creó correctamente')
             
                return redirect('home')  # Redirigir para evitar reenviar el formulario
            except:
                # Usar mensaje de error si el usuario ya existe
                messages.error(request, 'El usuario ya existe')
                return redirect('registro')
            
        else:
            # Usar mensaje de error si las contraseñas no coinciden
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('registro')
    
    return render(request, 'registro.html', {'form': UserCreationForm})

@login_required
def cerrar_sesion (request):
    logout(request)
    return redirect('inicio_sesion')

def inicio_sesion(request):
    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm()  # Correcta instanciación del formulario
        })
    else:
        # Obtener los datos del formulario POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autenticación del usuario
        user = authenticate(request, username=username, password=password)
        
        # Si la autenticación falla
        if user is None:
            messages.info(request, 'Usuario o contraseña incorrectos. ¡Intente de nuevo!')
            return render(request, 'login.html', {'form': AuthenticationForm()})
        else:
            # Si la autenticación es exitosa, iniciar sesión
            login(request, user)
            return redirect('home')  # Redirigir a la página de inicio después de iniciar sesión
        

def solicitudes(request):
    # Si el usuario es de la matriz, mostrar todas las solicitudes
    if request.user.es_matriz:
        solicitudes = Solicitud.objects.all()
    else:
        # Si es de una sucursal, solo mostrar las solicitudes de esa sucursal
        solicitudes = Solicitud.objects.filter(usuario__sucursal=request.user.sucursal)

    return render(request, 'solicitudes/lista_solicitudes.html', {
        'solicitudes': solicitudes
    })
    
def solicitudes_por_sucursal(request, sucursal_id):
    sucursal = Sucursal.objects.get(id=sucursal_id)
    solicitudes = Solicitud.objects.filter(usuario__sucursal=sucursal)
    
    return render(request, 'solicitudes/lista_solicitudes.html', {
        'solicitudes': solicitudes
    })
  
@login_required
def crear_solicitud(request):
    if request.method == 'POST':
        # Cargar los formularios con los datos enviados por POST
        form = SolicitudForm(request.POST, prefix='solicitud')
        conyuge_form = SolicitudConyugeForm(request.POST, prefix='conyuge')
        info_form = InfoForm(request.POST, prefix='info')
        credi_form = CreditoForm(request.POST, prefix='credi')
        ref_bancos_form = BancosForm(request.POST, prefix='ref_bancos')
        ref_personal_form = ReferenciasPersonalesForm(request.POST, prefix='ref_personal')
        ref_bancaria_form = ReferenciasBancariasForm(request.POST, prefix='ref_bancaria')
        contactos_form = ContactosForm(request.POST, prefix='contactos')

        print("Datos recibidos:", request.POST)  # Depuración

        # Validar los formularios principales
        if form.is_valid() and conyuge_form.is_valid() and info_form.is_valid() and credi_form.is_valid():
            try:
                with transaction.atomic():  # Iniciar una transacción
                    solicitud = form.save()

                    conyuge = conyuge_form.save(commit=False)
                    conyuge.solicitud = solicitud
                    conyuge.save()

                    info = info_form.save(commit=False)
                    info.solicitud = solicitud
                    info.save()

                    credi = credi_form.save(commit=False)
                    credi.solicitud = solicitud
                    credi.save()

                    # Procesar referencias y contactos
                    bancos_data_json = request.POST.get('bancos-data')
                    if bancos_data_json:
                        bancos_data = json.loads(bancos_data_json)
                        for banco_data in bancos_data:
                            DatosBanco.objects.create(
                                solicitud=solicitud,
                                banco=banco_data.get('id_ref_bancos-banco'),
                                cuenta_banco=banco_data.get('id_ref_bancos-cuenta_banco'),
                                clabe_interbancaria=banco_data.get('id_ref_bancos-clabe_interbancaria'),
                                rfc=banco_data.get('id_ref_bancos-rfc'),
                                no_tarjeta=banco_data.get('id_ref_bancos-no_tarjeta')
                            )

                    personales_data_json = request.POST.get('referencias-data')
                    if personales_data_json:
                        personales_data = json.loads(personales_data_json)
                        for personal_data in personales_data:
                            ReferenciasPersonales.objects.create(
                                solicitud=solicitud,
                                nombre=personal_data.get('id_ref_personal-nombre'),
                                direccion=personal_data.get('id_ref_personal-direccion'),
                                relacion=personal_data.get('id_ref_personal-relacion'),
                                telefono=personal_data.get('id_ref_personal-telefono')
                            )

                    bancarias_data_json = request.POST.get('bancarias-data')
                    if bancarias_data_json:
                        bancaria_data = json.loads(bancarias_data_json)
                        for bancarias_data in bancaria_data:
                            ReferenciasBancarias.objects.create(
                                solicitud=solicitud,
                                institucion=bancarias_data.get('id_ref_bancaria-institucion'),
                                direccion_institucion=bancarias_data.get('id_ref_bancaria-direccion_institucion'),
                                no_cuenta=bancarias_data.get('id_ref_bancaria-no_cuenta'),
                                tipo_cuenta=bancarias_data.get('id_ref_bancaria-tipo_cuenta'),
                                telefono_institucion=bancarias_data.get('id_ref_bancaria-telefono_institucion'),
                                tipo_ref=bancarias_data.get('id_ref_bancaria-tipo_ref')
                            )

                    contactos_data_json = request.POST.get('contactos-data')
                    if contactos_data_json:
                        contacto_data = json.loads(contactos_data_json)
                        for contactos_data in contacto_data:
                            Contactos.objects.create(
                                solicitud=solicitud,
                                apellido_paterno=contactos_data.get('id_contactos-apellido_paterno'),
                                apellido_materno=contactos_data.get('id_contactos-apellido_materno'),
                                nombres=contactos_data.get('id_contactos-nombres'),
                                puesto=contactos_data.get('id_contactos-puesto'),
                                email=contactos_data.get('id_contactos-email'),
                                telefono=contactos_data.get('id_contactos-telefono')
                            )

                messages.success(request, "Solicitud creada exitosamente.")
                return redirect('home')

            except Exception as e:
                print(f"Error al guardar la solicitud: {e}")
                messages.error(request, f"Error al guardar la solicitud: {e}")
                form.add_error(None, "Ocurrió un error al procesar la solicitud. Inténtalo nuevamente.")

        else:
            print("Errores en los formularios principales:")
            print(form.errors)
            print(conyuge_form.errors)
            print(info_form.errors)
            print(credi_form.errors)
  
    else:
        # Inicializar los formularios en caso de GET
        form = SolicitudForm(prefix='solicitud')
        conyuge_form = SolicitudConyugeForm(prefix='conyuge')
        info_form = InfoForm(prefix='info')
        credi_form = CreditoForm(prefix='credi')
        ref_bancos_form = BancosForm(prefix='ref_bancos')
        ref_personal_form = ReferenciasPersonalesForm(prefix='ref_personal')
        ref_bancaria_form = ReferenciasBancariasForm(prefix='ref_bancaria')
        contactos_form = ContactosForm(prefix='contactos')

    return render(request, 'crear_solicitud.html', {
        'form': form,
        'conyuge_form': conyuge_form,
        'info_form': info_form,
        'credi_form': credi_form,
        'ref_bancos_form': ref_bancos_form,
        'ref_personal_form': ref_personal_form,
        'ref_bancaria_form': ref_bancaria_form,
        'contactos_form': contactos_form
    })


def obtener_datos_cp(request):
    codigo_postal = request.GET.get('codigo_postal', None)
    if codigo_postal:
        # Filtramos los códigos postales
        codigos = CodigoPostal.objects.filter(codigo_postal=codigo_postal)
        if codigos.exists():
            # Usar una lista para almacenar colonias
            colonias = []
            for codigo in codigos:
                # Agregar la colonia a la lista, si no está ya presente
                colonias.append({
                    'id': codigo.id,  # ID de la colonia
                    'nombre': codigo.colonia,
                })

            # Usar el primer resultado para obtener estado y municipio
            primer_codigo = codigos.first()
            data = {
                'estado': primer_codigo.estado,
                'municipio': primer_codigo.municipio,
                'colonias': colonias,
            }
        else:
            data = {'error': 'Código postal no encontrado'}
    else:
        data = {'error': 'No se envió código postal'}
    
    return JsonResponse(data)


@login_required
def tabla_datos(request):
    query = request.GET.get('query')  # Obtener el término de búsqueda

    # Filtrar los resultados según la búsqueda y el estado
    if query:
        datos = Solicitud.objects.filter(
            Q(nombres__icontains=query) | Q(rfc__icontains=query)
        )
    else:
        datos = Solicitud.objects.all()  # Si no hay búsqueda, se muestran todos

    return render(request, 'tabla_datos.html', {
        'datos': datos
    })

@login_required
def generate_pdf(request):
    if request.method == 'POST':
        # Obtener datos del cliente y amortización (ejemplo estático)
        data = json.loads(request.body).get('tableData', [])

        # Crear el objeto de respuesta PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="amortization_table.pdf"'

        # Crear un documento PDF
        pdf = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Crear un estilo para el título
        title_style = ParagraphStyle(
            name='TitleStyle',
            fontSize=18,
            spaceAfter=20,
            alignment=1  # Centrar título
        )
        title = Paragraph("Tabla de Amortización", title_style)
        elements.append(title)

        # Crear detalles adicionales
        client_info = [
            ["Institución:", "SISU S.A. DE C.V. SOFOM ENR", "", "Fecha de Elaboración:", datetime.now().strftime("%d/%b/%Y")],
            ["Nombre del Cliente:", "[NOMBRE DEL ACREDITADO]", "", "No. Crédito:", "123456"],
            ["Producto:", "Crédito Personal", "", "Saldo Inicial:", "$10,000.00"],
            ["Plazo:", "12", "", "Periodicidad de Pago:", "Quincenal"]
        ]
        client_table = Table(client_info, colWidths=[100, 180, 20, 150, 100])
        client_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(client_table)

  
        # Añadir encabezados de la tabla
        headers = ["No. Pago", "F. pago", "IVA int.", "Interés", "Comisión", "Seguro", "Pago", "Capital", "Saldo Restante"]
        data.insert(0, headers)  # Insertar encabezados en los datos

        # Crear la tabla
        table = Table(data)

        # Establecer estilo de la tabla
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fondo gris para el encabezado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Texto blanco para el encabezado
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centrar texto
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fuente negrita para encabezados
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espaciado en el encabezado
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fondo beige para el resto de las filas
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordes de la tabla
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),  # Fuente normal para las celdas
            ('FONTSIZE', (0, 0), (-1, -1), 10),  # Tamaño de fuente
            ('TOPPADDING', (0, 0), (-1, -1), 10),  # Espaciado en celdas
        ])
        table.setStyle(style)


        elements.append(table)

        # Construir el PDF
        pdf.build(elements)

        return response

    return HttpResponse(status=400)


@login_required
def generate_contract_pdf(request):
    if request.method == 'POST':
        # Configuración del nombre del archivo PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="contrato_credito.pdf"'

        # Crear documento PDF
        pdf = SimpleDocTemplate(response, pagesize=letter, topMargin=40, bottomMargin=40)

        # Estilos de texto
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            name='TitleStyle', fontSize=18, alignment=1, spaceAfter=20, textColor=colors.darkblue
        )
        subtitle_style = ParagraphStyle(
            name='SubtitleStyle', fontSize=12, spaceAfter=12, textColor=colors.black, leading=15
        )
        normal_style = ParagraphStyle(
            name='NormalStyle', fontSize=11, leading=14, spaceAfter=12
        )

        # Lista de elementos del documento
        elements = []

        # LOGO
        logo_path = os.path.join("static", "img", "sisu.jpg")  # Ruta al logo
        if os.path.exists(logo_path):
            logo = Image(logo_path, width=120, height=60)
            logo.hAlign = 'CENTER'
            elements.append(logo)
            elements.append(Spacer(1, 20))

        # Título
        title = Paragraph("Contrato de Crédito Financiero", title_style)
        elements.append(title)

        # Fecha del contrato
        current_date = datetime.now().strftime('%d de %B de %Y')
        date = Paragraph(f"Fecha: {current_date}", subtitle_style)
        elements.append(date)

        # Información principal del contrato
        contract_content = """
        Este contrato de crédito financiero se celebra entre las siguientes partes:

        **Acreditante**: La SOFOM <b>[Nombre de la Institución]</b>, representada por su representante legal <b>[Nombre del Representante]</b>.
        
        **Acreditado**: <b>[Nombre del Cliente]</b>, identificado con <b>[Documento de Identidad]</b>.

        Las partes acuerdan las siguientes cláusulas:
        """
        elements.append(Paragraph(contract_content, normal_style))

        # Cláusulas del contrato
        clauses = [
            ["1. Objeto del Contrato", "La entidad otorga un crédito al cliente por un monto de $[Monto]."],
            ["2. Plazo y Condiciones de Pago", "El cliente se compromete a pagar el monto total en un plazo de [Plazo]."],
            ["3. Tasa de Interés", "La tasa de interés ordinaria aplicable será del [Tasa]% anual."],
            ["4. Gastos Adicionales", "Incluye costos por seguros, comisiones y otros servicios descritos en la tabla de amortización."],
            ["5. Incumplimiento", "En caso de incumplimiento, se aplicarán las penalidades correspondientes según lo estipulado."],
            ["6. Legislación Aplicable", "Este contrato está sujeto a las leyes de [Jurisdicción]."]
        ]

        # Tabla con las cláusulas
        table_data = [[Paragraph(f"<b>{clause[0]}</b>", normal_style), Paragraph(clause[1], normal_style)] for clause in clauses]
        table = Table(table_data, colWidths=[200, 300])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))
        elements.append(table)

        elements.append(Spacer(1, 30))

        # Tabla para las firmas
        firma_data = [
            ["_____________________________", "_____________________________"],
            ["Representante Legal", "Cliente"]
        ]

        firma_table = Table(firma_data, colWidths=[250, 250], hAlign='CENTER')
        firma_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Centra todo el contenido
            ('TOPPADDING', (0, 0), (-1, -1), 20),  # Espaciado superior
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),  # Espaciado inferior
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),  # Texto en negrita para los nombres
            ('FONTSIZE', (0, 1), (-1, 1), 10),  # Tamaño de fuente para los nombres
        ]))

        elements.append(firma_table)

        # Construir el PDF
        pdf.build(elements)

        return response

    return HttpResponse(status=400)


def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    if request.method == 'POST':
        solicitud.delete()
        messages.success(request, "Solicitud eliminada exitosamente.")
        return redirect('tabla_datos')  # Cambia al nombre de tu lista principal
    return redirect('tabla_datos')

@login_required
def cambiar_estado_solicitud(request, solicitud_id, nuevo_estado):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    print(f"Estado actual: {solicitud.status}")  # Depuración
    if nuevo_estado in dict(Solicitud.ESTADOS):
        solicitud.status = nuevo_estado
        solicitud.save()
        print(f"Nuevo estado: {solicitud.status}")  # Depuración
        messages.success(request, f"Estado cambiado a {nuevo_estado.capitalize()}.")
    else:
        messages.error(request, "Estado no válido.")
    return redirect('tabla_datos')


@login_required
def crear_credito(request):
    # Obtener todas las solicitudes con status 'alta', 'validacion' o 'credito'
    clientes_alta = Solicitud.objects.filter(status='alta')
    clientes_validacion = Solicitud.objects.filter(status='validacion')
    clientes_credito = Solicitud.objects.filter(status='aprobado')

    # Serializar los datos de las solicitudes
    clientes_alta_list = SolicitudSerializer(clientes_alta, many=True).data
    clientes_validacion_list = SolicitudSerializer(clientes_validacion, many=True).data
    clientes_credito_list = SolicitudSerializer(clientes_credito, many=True).data

    # Capturar ID de solicitud desde la petición (POST o GET)
    solicitud_id = (
        request.POST.get('solicitud_id_pld') or  # Captura desde el modal PLD
        request.POST.get('solicitud_id') or     # Captura desde el formulario principal
        request.GET.get('solicitud_id')
    )
    solicitud = Solicitud.objects.filter(id=solicitud_id).first() if solicitud_id else None

    # Obtener colonias disponibles
    colonias = Solicitud.objects.values_list('colonia', flat=True).distinct()

    if request.method == 'POST':
        # Validación de PLD activada
        if request.POST.get('validate_pld') == 'true':
            solicitud_id = request.POST.get('solicitud_id_pld')
            solicitud = Solicitud.objects.filter(id=solicitud_id).first()

            if solicitud:
                # Función para cargar la lista SDN desde el archivo CSV
                def cargar_lista_sdn():
                    sdn_list = []
                    try:
                        with open('D:/SOFOM_RESIDENCIA/sofom/sofom_project/data/sdn.csv', mode='r', encoding='utf-8') as file:
                            csv_reader = csv.reader(file)
                            next(csv_reader)  # Omitir encabezado
                            for row in csv_reader:
                                if len(row) > 1:
                                    sdn_list.append(row[1].strip())  # Columna 1: Nombres
                    except Exception as e:
                        print(f"Error al cargar la lista SDN: {e}")
                    return sdn_list

                # Cargar lista SDN
                lista_sdn = cargar_lista_sdn()
                nombre_cliente = solicitud.nombres.strip().upper()

                # Cotejo difuso con la lista SDN
                coincidencias_sdn = process.extract(nombre_cliente, lista_sdn, scorer=fuzz.token_sort_ratio)
                umbral = 80
                coincidencias_sdn_nombres = [nombre for nombre, score in coincidencias_sdn if score >= umbral]

                # Listas negras locales
                listas_negras_local = ["FERNANDO", "FIDEL ALEJANDRO", 'AL-AQSA']
                coincidencias_locales = [nombre for nombre in listas_negras_local if nombre in nombre_cliente]
              
                # Caso: Cliente rechazado
                if coincidencias_sdn_nombres or coincidencias_locales:
                    solicitud.status = 'rechazado'
                    solicitud.save()

                    # Registrar en lista negra
                    ListaNegra.objects.create(
                        solicitud=solicitud,
                        motivo="Coincidencia en listas negras (SDN o Locales)",
                        fecha_rechazo=timezone.now()
                    )

                    return JsonResponse({
                        'status': 'rechazado',
                        'message': 'El cliente está en una lista negra y ha sido rechazado.',
                        'coincidencias_local': coincidencias_locales,
                        'coincidencias_sdn': coincidencias_sdn_nombres
                    })

                # Caso: Cliente aprobado
                else:
                    # Actualizamos el estado de la solicitud
                    solicitud.status = 'aprobado'
                    solicitud.save()

                    return JsonResponse({
                        'status': 'aprobado',
                        'message': 'El cliente pasó la validación de PLD y se otorgó el crédito.'
                    })

            # Caso: No se encontró la solicitud
            return JsonResponse({
                'status': 'error',
                'message': 'No se encontró la solicitud para validación.'
            })


        # Crear o actualizar la solicitud con los datos enviados
        form = SolicitudForm(request.POST, instance=solicitud, prefix='solicitud')
        if form.is_valid():
            try:
                form.save()
                if solicitud:
                    solicitud.status = 'validacion'
                    solicitud.save()
                messages.success(request, 'Solicitud guardada y movida a validación exitosamente.')
                return redirect('crear_credito')
            except Exception as e:
                messages.error(request, f'Error al guardar la solicitud: {e}')
        else:
            messages.error(request, 'Hay errores en el formulario. Verifique los datos ingresados.')

    else:
        form = SolicitudForm(instance=solicitud, prefix='solicitud')

    return render(request, 'crear_credito.html', {
        'clientes_alta': json.dumps(clientes_alta_list, cls=DjangoJSONEncoder),
        'clientes_validacion': json.dumps(clientes_validacion_list, cls=DjangoJSONEncoder),
        'clientes_credito': json.dumps(clientes_credito_list, cls=DjangoJSONEncoder),
        'form': form,
        'colonias': colonias,
    })


def cargar_cliente(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, id=solicitud_id)
    return render(request, 'crear_credito.html', {'solicitud': solicitud})

   
@login_required
def exportar_excel(request):
    # Crear una respuesta HTTP con el tipo de contenido de un archivo Excel
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="reporte_clientes.xls"'

    # Crear un libro de trabajo Excel
    libro = xlwt.Workbook()
    hoja = libro.add_sheet('Reporte Clientes')

    # Agregar un encabezado a la hoja de Excel
    hoja.write(0, 0, 'Apellido Paterno')
    hoja.write(0, 1, 'Apellido Materno')
    hoja.write(0, 2, 'Nombre')
    hoja.write(0, 3, 'Cónyuge')
    hoja.write(0, 4, 'Edad')
    hoja.write(0, 5, 'RFC')
    hoja.write(0, 6, 'Género')
    
    # Agregar la leyenda al principio del archivo
    hoja.write(1, 0, 'REPORTE GENERAL DE TODOS LOS CLIENTES')
    
    # Obtener los datos de la base de datos
    solicitudes = Solicitud.objects.all()

    # Agregar los datos de las solicitudes a la hoja de Excel
    for i, solicitud in enumerate(solicitudes, start=2):
        hoja.write(i, 0, solicitud.apellido_paterno)
        hoja.write(i, 1, solicitud.apellido_materno)
        hoja.write(i, 2, solicitud.nombres)
        hoja.write(i, 3, ', '.join([f"{conyuge.nombres} {conyuge.apellido_paterno}" for conyuge in solicitud.conyuge.all()]) if solicitud.conyuge.all() else 'No tiene conyuge')
        hoja.write(i, 4, solicitud.edad)
        hoja.write(i, 5, solicitud.rfc)
        hoja.write(i, 6, solicitud.genero)
    
    # Guardar y devolver el archivo Excel como respuesta
    libro.save(response)
    return response

   
