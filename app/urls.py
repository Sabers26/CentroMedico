from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('addColaboradores', addColaboradores, name='addColaboradores'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('listado', listado, name='listado'),
    path('eliminar/<rut>/<estado>', eliminar, name='eliminar'),
    path('modificarusuario/<rut>/<tipo>', modificarusuario, name='modificarusuario'),
    path('toma-fecha',tomaFecha,name='toma-fecha'),
    path('tomahorario/<fecha>/<especialidad>/<rut>',tomaHorario,name='tomahorario'),
    path('registrohorario/<rut>', registrohorario, name='registrohorario'),
    path('resumen/<rut_medico>/<rut_paciente>/<fecha>/<id_horario>/', resumen, name='resumen'),
    path('buscarAtencion', buscarAtencion, name='buscarAtencion'),
    path('listadoHorarioMedico/<rut>', listadoHorarioMedico, name='listadoHorarioMedico'),
    path('eliminarhorario/<fecha>/<id>/<rut>/<observacion>', eliminarhorario, name='eliminarhorario'),
    path('lista_usuarios',lista_usuarios, name='lista_usuarios'),
    path('atencion/<rut_medico>/<rut_paciente>/<fecha>/<id_horario>/<correo>',atencion, name='atencion'),
    path('lista_atenciones/<rut>',lista_atenciones, name='lista_atenciones'),
    path('eliminar_atencion/<ida>/<rut>/<fecha>/<idh>/<rutpa>',eliminar_atencion, name='eliminar_atencion'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    ]
