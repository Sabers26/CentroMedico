from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('addColaboradores', addColaboradores, name='addColaboradores'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('listado', listado, name='listado'),
    path('modifiColab/<id>', modifiColab, name='modifiColab'),
    path('eliminar/<id>/<estado>', eliminar, name='eliminar'),
    path('modificarusuario/<id>', modificarusuario, name='modificarusuario'),
    path('horario',horario,name='horario'),
    path('toma-fecha',tomaFecha,name='toma-fecha'),
    path('toma-horario/<fecha>/<especialidad>',tomaHorario,name='toma-horario'),
    path('registrohorario/<id>', registrohorario, name='registrohorario'),
    path('resumen/<data>', resumen, name='resumen'),
    path('buscarAtencion', buscarAtencion, name='buscarAtencion'),
    path('listadoHorarioMedico/<id>', listadoHorarioMedico, name='listadoHorarioMedico'),
    path('confirmaciontoma<data>', confirmaciontoma, name='confirmaciontoma'),
    path('eliminarhorario/<data>', resumen, name='resumen'),
]