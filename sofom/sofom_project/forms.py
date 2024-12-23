from django import forms
from .models import Solicitud, Solicitud_conyuge, Info_solicitante, DatosBanco, ReferenciasPersonales, ReferenciasBancarias, Contactos, Datos_Credito, Credito
from rest_framework import serializers


class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = '__all__' 
        
class SolicitudForm(forms.ModelForm):
    class Meta:
        model = Solicitud
        fields = '__all__'
        widgets = {
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'dependientes': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_id_oficial': forms.Select(attrs={'class': 'form-select'}),
            'clave_id_oficial': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'class': 'form-control'}),
            'nacionalidad': forms.Select(attrs={'class': 'form-select'}),
            'pais_nacimiento': forms.Select(attrs={'class': 'form-select'}),
            'entidad_federativa_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'proveedor_recursos': forms.TextInput(attrs={'class': 'form-control'}),
            'mercado': forms.Select(attrs={'class': 'form-select'}),
            'imss': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control','maxlength': '5','placeholder': 'Ingresa el código postal'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'colonia': forms.Select(attrs={'class': 'form-select'}),
            'calle': forms.TextInput(attrs={'class': 'form-control'}),
            'no_exterior': forms.TextInput(attrs={'class': 'form-control'}),
            'no_interior': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad_poblacion': forms.TextInput(attrs={'class': 'form-control'}),
            'entre_calles': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_vivienda': forms.Select(attrs={'class': 'form-select'}),
            'anios_residencia': forms.Select(attrs={'class': 'form-select'}),
            'telefono_fijo': forms.TextInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_avisos': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

        
class SolicitudConyugeForm(forms.ModelForm):
    class Meta:
        model = Solicitud_conyuge
        fields = ['apellido_paterno','apellido_materno','nombres','fecha_nacimiento','edad','rfc','genero','lugar_nacimiento',
            'profesion','nombre_empresa','puesto','fecha_ingreso','antiguedad']
        
        widgets = {
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'genero': forms.Select(attrs={'class': 'form-select'}),
            'lugar_nacimiento': forms.TextInput(attrs={'class': 'form-control'}),
            'profesion': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'antiguedad': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
    }   
   
class InfoForm(forms.ModelForm):
    class Meta:
        model = Info_solicitante
        fields = ['nombre_empresa','puesto','antiguedad','calle','no_exterior','no_interior','soli_codigo_postal',
            'soli_estado','soli_municipio','soli_colonia','telefono','ext','no_empleado','nombre_jefe','ingreso_mensual','descuento','ingreso_neto',
            'ingresos_no_comprobables'
            ]
        
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class':'form-control'}),
            'puesto' : forms.TextInput(attrs={'class':'form-control'}),
            'antiguedad' : forms.TextInput(attrs={'class':'form-control'}),
            'calle': forms.TextInput(attrs={'class':'form-control'}),
            'no_exterior' : forms.TextInput(attrs={'class':'form-control'}),
            'no_interior' : forms.TextInput(attrs={'class':'form-control'}),
            'soli_codigo_postal': forms.TextInput(attrs={'class': 'form-control','maxlength': '5','placeholder': 'Ingresa el código postal'}),
            'soli_estado': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'soli_municipio': forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'soli_colonia': forms.Select(attrs={'class': 'form-select'}),
            'telefono' : forms.TextInput(attrs={'class': 'form-control'}),
            'ext' : forms.TextInput(attrs={'class': 'form-control'}),
            'no_empleado' : forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_jefe' : forms.TextInput(attrs={'class': 'form-control'}),
            'ingreso_mensual' : forms.TextInput(attrs={'class': 'form-control'}),
            'descuento' : forms.TextInput(attrs={'class': 'form-control'}),
            'ingreso_neto' : forms.TextInput(attrs={'class': 'form-control', 'readonly':'readonly'}),
            'ingresos_no_comprobables' : forms.TextInput(attrs={'class': 'form-control'}),
           
        
}
        
class BancosForm(forms.ModelForm):
    class Meta:
        model = DatosBanco
        fields = ['banco', 'cuenta_banco', 'clabe_interbancaria', 'rfc', 'no_tarjeta']
        widgets = {
            'banco': forms.TextInput(attrs={'class': 'form-control'}),
            'cuenta_banco': forms.TextInput(attrs={'class': 'form-control'}),
            'clabe_interbancaria': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'no_tarjeta': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BancosForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # Desactiva la validación obligatoria

         
class ReferenciasPersonalesForm(forms.ModelForm):
    class Meta:
        model = ReferenciasPersonales
        fields = ['nombre', 'direccion', 'relacion', 'telefono']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'relacion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReferenciasPersonalesForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # Desactiva la validación obligatoria
            
class ReferenciasBancariasForm(forms.ModelForm):
    class Meta:
        model = ReferenciasBancarias
        fields = ['institucion', 'direccion_institucion', 'no_cuenta', 'tipo_cuenta', 'telefono_institucion', 'tipo_ref']
        widgets = {
            'institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'no_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_cuenta': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_institucion': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_ref': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(ReferenciasBancariasForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # Desactiva la validación obligatoria

        
class CreditoForm(forms.ModelForm):
    class Meta:
        model = Datos_Credito
        fields = ['tipo_credito', 'monto_prestamo', 'periodo_pago', 'numero_periodos', 'moneda', 'destino_credito', 'descripcion']
        widgets = {
            'tipo_credito': forms.Select(attrs={'class': 'form-select'}),
            'monto_prestamo': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'numero_periodos': forms.Select(attrs={'class': 'form-select'}),
            'moneda': forms.Select(attrs={'class': 'form-select'}),
            'destino_credito': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContactosForm(forms.ModelForm):
    class Meta:
        model = Contactos
        fields = ['apellido_paterno', 'apellido_materno', 'nombres', 'puesto', 'email', 'telefono']
        widgets = {
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(ContactosForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # Desactiva la validación obligatoria
            
class CreditoOtorgadoForm(forms.ModelForm):
    class Meta:
        model = Credito
        fields = ['tipo_credito', 'periodo_pago', 'numero_periodos', 'fecha_inicio','fecha_final','num_pagos','moneda','monto', 'comision', 'seguro', 'iva', 'estado', 'tasa_interes', 'fecha_aprobacion', 'fecha_entrega']
        widgets = {
            'tipo_credito': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Ingresa el tipo de credito'}),
            'periodo_pago': forms.Select(attrs={'class': 'form-select'}),
            'numero_periodos': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_final': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'num_pagos': forms.NumberInput(attrs={'class': 'form-control'}),
            'moneda': forms.Select(attrs={'class': 'form-select','placeholder': 'Moneda'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monto del crédito'}),
            'comision': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Comision'}),
            'seguro': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Seguro'}),
            'iva': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'IVA'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'tasa_interes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tasa de interés (%)'}),
            'fecha_aprobacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
