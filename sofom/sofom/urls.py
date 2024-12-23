"""
URL configuration for sofom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sofom_project import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.inicio_sesion, name='inicio_sesion'),
    path('registro', views.registro, name='registro'),
    path('home/', views.home, name='home'),
    path('salir/', views.cerrar_sesion, name='cerrar_sesion'),
    path('crear-solicitud/', views.crear_solicitud, name='crear_solicitud'),
    path('obtener-datos-cp/', views.obtener_datos_cp, name='obtener_datos_cp'),
    path('tabla-datos/', views.tabla_datos, name='tabla_datos'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('generate_contract_pdf/', views.generate_contract_pdf, name='generate_pdf'),
    path('eliminar-solicitud/<int:solicitud_id>/', views.eliminar_solicitud, name='eliminar_solicitud'),
    path('cambiar-estado/<int:solicitud_id>/<str:nuevo_estado>/', views.cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
    path('crear-credito/', views.crear_credito, name='crear_credito'),
    path('exportar_excel/', views.exportar_excel, name='exportar_excel'),
   
 


]
