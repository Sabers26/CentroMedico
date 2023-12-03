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
    path('toma-horario',tomaHorario,name='toma-horario'),
    path('registrohorario/<rut>', registrohorario, name='registrohorario'),
    path('resumen', resumen, name='resumen'),
    path('buscarAtencion', buscarAtencion, name='buscarAtencion'),
    path('listadoHorarioMedico/<rut>', listadoHorarioMedico, name='listadoHorarioMedico'),
    path('confirmaciontoma', confirmaciontoma, name='confirmaciontoma'),
    path('eliminarhorario/<fecha>/<id>/<rut>/<observacion>', eliminarhorario, name='eliminarhorario'),
    path('lista_usuarios',lista_usuarios, name='lista_usuarios'),
    ]
