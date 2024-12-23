from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import date
from django.utils import timezone
from .datos import PAISES, ANOS_RESIDENCIA, TIPO_CREDITO

# Create your models here.
class Solicitud(models.Model):
    ESTADOS = [
        ('prospecto', 'Prospecto'),
        ('alta', 'Dada de Alta'),
    ]
    status = models.CharField(max_length=20, choices=ESTADOS, default='prospecto', blank=True, null=True)  # Nuevo campo
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True) 
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    nombres = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()
    rfc = models.CharField(max_length=12)
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    estado_civil = models.CharField(max_length=3, choices=[
        ('Sol', 'Soltero(a)'), 
        ('Cas', 'Casado(a)'), 
        ('Viu', 'Viudo(a)'), 
        ('Uni', 'Unión libre'),
        ('Div', 'Divorciado(a)')
    ])
    dependientes = models.IntegerField()
    tipo_id_oficial = models.CharField(max_length=3, choices=[
        ('INE', 'INE'), 
        ('CM', 'Cartilla Militar'), 
        ('PAS', 'Pasaporte')
    ])
    clave_id_oficial = models.CharField(max_length=50)
    curp = models.CharField(max_length=18)
    nacionalidad = models.CharField(max_length=50, choices=[
        ('MX', 'Mexicana'),
        ('US', 'Extranjera')
    ])
    pais_nacimiento = models.CharField(max_length=50, choices=PAISES)
    entidad_federativa_nacimiento = models.CharField(max_length=50)
    proveedor_recursos = models.CharField(max_length=100)
    mercado = models.CharField(max_length=3, choices=[
        ('AB', 'Abierto'),
        ('EDG', 'Empresa del grupo'),
        ('CCA', 'Cliente Cautivo'),
        ('REC', 'Recomendado')
    ])
    imss = models.CharField(max_length=11, blank=True, null=True)
    
    # Información de domicilio
    codigo_postal = models.CharField(max_length=5)
    estado = models.CharField(max_length=50)
    municipio = models.CharField(max_length=100)
    colonia = models.CharField(max_length=100)
    calle = models.CharField(max_length=100)
    no_exterior = models.CharField(max_length=10, blank=True, null=True)
    no_interior = models.CharField(max_length=10, blank=True, null=True)
    entre_calles = models.CharField(max_length=200)
    tipo_vivienda = models.CharField(max_length=3, choices=[
        ('PR', 'Propia'),
        ('RE', 'Rentada')
    ])
    anios_residencia = models.CharField(max_length=50, choices=ANOS_RESIDENCIA)
    
    # Información de contacto
    telefono_fijo = models.CharField(max_length=15, blank=True, null=True)
    celular = models.CharField(max_length=15)
    telefono_avisos = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return f'{self.nombres} {self.apellido_paterno} {self.apellido_materno}'

class Solicitud_conyuge(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='conyuge')  # Relación con Solicitud
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    nombres = models.CharField(max_length=200)
    fecha_nacimiento = models.DateField()
    edad = models.IntegerField()
    rfc = models.CharField(max_length=12)
    genero = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    lugar_nacimiento = models.CharField(max_length=100)
    profesion = models.CharField(max_length=100)
    nombre_empresa = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    antiguedad = models.CharField(max_length=12, blank=True)
    def save(self, *args, **kwargs):
        # Calcular antigüedad
        today = date.today()
        delta = today - self.fecha_ingreso
        years = delta.days // 365
        self.antiguedad = f'{years} años'
        super(Solicitud_conyuge, self).save(*args, **kwargs)

class Info_solicitante(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='info')  # Relación con Solicitud
    nombre_empresa = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    antiguedad = models.CharField(max_length=50)
    calle = models.CharField(max_length=100)
    no_exterior = models.CharField(max_length=10, blank=True, null=True)
    no_interior = models.CharField(max_length=10, blank=True, null=True)
    soli_codigo_postal = models.CharField(max_length=5)
    soli_estado = models.CharField(max_length=50)
    soli_municipio = models.CharField(max_length=100)
    soli_colonia = models.CharField(max_length=100)
    telefono = models.IntegerField()
    ext = models.CharField(max_length=20)
    no_empleado = models.IntegerField()
    nombre_jefe = models.CharField(max_length=100)
    ingreso_mensual = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2)
    ingreso_neto = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        # Calcular ingreso neto
        self.ingreso_neto = self.ingreso_mensual - self.descuento
        super(Info_solicitante, self).save(*args, **kwargs)
    ingresos_no_comprobables = models.DecimalField(max_digits=10, decimal_places=2)
    
class DatosBanco(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='datos_banco')
    banco = models.CharField(max_length=100, blank=True)  # blank=True para permitir campos vacíos en el formulario
    cuenta_banco = models.IntegerField(blank=True, null=True)  # Si puede ser opcional
    clabe_interbancaria = models.IntegerField(blank=True, null=True)
    rfc = models.CharField(max_length=12, blank=True)
    no_tarjeta = models.IntegerField(blank=True, null=True)
    
class ReferenciasPersonales(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='referenciasP')
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    relacion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)  # Cambiado a CharField para números de teléfono

class ReferenciasBancarias(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='referenciasB') 
    institucion = models.CharField(max_length=100, blank=True, null=True)  # Opcional
    direccion_institucion = models.CharField(max_length=100, blank=True, null=True)  # Opcional
    no_cuenta = models.IntegerField(blank=True, null=True)  # Opcional
    tipo_cuenta = models.CharField(max_length=100, blank=True, null=True)  # Opcional
    telefono_institucion = models.CharField(max_length=20, blank=True, null=True)  # Cambiado a CharField
    TIPO_REFERENCIA_CHOICES = [
        ('personal', 'Personal'),
        ('bancaria', 'Bancaria'),
        ('comercial', 'Comercial'),
        ('auto empleo', 'Auto empleo'),
        ('asalariado', 'Asalariado')
    ]
    tipo_ref = models.CharField(max_length=20, choices=TIPO_REFERENCIA_CHOICES)

    def __str__(self):
        return f'{self.nombre} - {self.tipo_ref}'
    
class Datos_Credito(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='datos_credito')  # Relación con Solicitud
    tipo_credito = models.CharField(max_length=50, choices=TIPO_CREDITO, null=False, blank=False)
    monto_prestamo = models.IntegerField()   
    # Campo que especifica si el pago es quincenal o mensual
    periodo_pago = models.CharField(max_length=10, choices=[
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
        ('SEMANAL', 'Semanal')
    ])
    
    # Este campo almacenará el número de períodos (quincenas o meses)
    numero_periodos = models.PositiveIntegerField()  # Aquí almacenamos el número de quincenas o meses
    
    moneda = models.CharField(max_length=50, choices=[('MXN', 'NACIONAL')])
    destino_credito = models.CharField(max_length=50, choices=[
        ('CASA', 'Compra de casa'),
        ('CARRO', 'Compra de carro'),
        ('TERRENO', 'Compra de terreno'),
        ('COLEGIATURAS', 'Colegiaturas'),
        ('GASTOS PERSONALES', 'Gastos personales'),
        ('INVERSION', 'Inversion'),
        ('GASOTOS MEDICOS','Gastos Medicos')
    ])
    descripcion = models.CharField(max_length=200)
     # Campo que almacena la fecha de otorgamiento del crédito
    fecha_otorgamiento = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.tipo_credito} - {self.monto_prestamo} {self.moneda}"
    
class Contactos(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='contactos')  # Relación con Solicitud
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    nombres = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20) 
    
class CodigoPostal(models.Model):
    codigo_postal = models.CharField(max_length=5)
    estado = models.CharField(max_length=100)
    municipio = models.CharField(max_length=100)
    colonia = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo_postal} - {self.colonia}"

#Modelos para sucursal 
class Sucursal(models.Model):
    nombre = models.CharField(max_length=20)
    direccion = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    
    def __str__(self):
        return self.nombre
   

class Usuario(AbstractUser):
    sucursal = models.ForeignKey('Sucursal', on_delete=models.CASCADE, related_name='usuarios', null=True, blank=True)
    es_matriz = models.BooleanField(default=False)

    # Resolver el conflicto de relaciones reversas
    groups = models.ManyToManyField(
        Group,
        related_name='usuarios_grupo',  # Cambia el nombre de la relación reversa
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_permiso',  # Cambia el nombre de la relación reversa
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Credito(models.Model):
    ESTADOS_CREDITO = [
        ('elaboracion', 'Elaboración'),
        ('evaluacion', 'Evaluación'),
        ('autorizacion', 'Autorización'),
        ('instrumentacion', 'Instrumentación'),
        ('entregado', 'Entregado')
    ]
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE, related_name='creditos')
    tipo_credito = models.CharField(max_length=50, choices=TIPO_CREDITO)
    # Campo que especifica si el pago es quincenal o mensual
    periodo_pago = models.CharField(max_length=10, choices=[
        ('QUINCENAL', 'Quincenal'),
        ('MENSUAL', 'Mensual'),
        ('SEMANAL', 'Semanal')
    ]) 
    # Este campo almacenará el número de períodos (quincenas o meses)
    numero_periodos = models.PositiveIntegerField()  # Aquí almacenamos el número de quincenas o meses 
    moneda = models.CharField(max_length=50, choices=[('MXN', 'NACIONAL')])
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_inicio = models.DateField() 
    fecha_final = models.DateField()
    num_pagos = models.IntegerField()
    comision = models.IntegerField()
    seguro = models.IntegerField()
    iva = models.IntegerField()
    estado = models.CharField(max_length=15, choices=ESTADOS_CREDITO, default='elaboracion')
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_aprobacion = models.DateField()
    fecha_entrega = models.DateField()
    # Otros campos relevantes para el crédito

    def __str__(self):
        return f"Crédito para {self.solicitud.nombre_cliente} - Estado: {self.estado}"
    
class ListaNegra(models.Model):
    solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
    motivo = models.CharField(max_length=255)
    fecha_rechazo = models.DateTimeField(auto_now_add=True)
