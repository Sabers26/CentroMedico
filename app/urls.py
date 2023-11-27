from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('addColaboradores', addColaboradores, name='addColaboradores'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('listado', listado, name='listado'),
    path('modifiColab', modifiColab, name='modifiColab'),
    path('eliminar', eliminar, name='eliminar'),
    path('modificarusuario', modificarusuario, name='modificarusuario'),
    path('horario',horario,name='horario'),
    path('toma-fecha',tomaFecha,name='toma-fecha'),
    path('toma-horario',tomaHorario,name='toma-horario'),
    path('registrohorario', registrohorario, name='registrohorario'),
    path('resumen', resumen, name='resumen'),
    path('buscarAtencion', buscarAtencion, name='buscarAtencion'),
    path('listadoHorarioMedico', listadoHorarioMedico, name='listadoHorarioMedico'),
    path('confirmaciontoma', confirmaciontoma, name='confirmaciontoma'),
    path('eliminarhorario', resumen, name='resumen'),]
