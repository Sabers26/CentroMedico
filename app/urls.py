from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('addColaboradores', addColaboradores, name='addColaboradores'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('listado', listado, name='listado'),
    path('eliminar', eliminar, name='eliminar'),
    path('modifiColab', modifiColab, name='modifiColab'),
]