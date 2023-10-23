from django.urls import path
from .views import *

urlpatterns = [
    path('', inicio, name='inicio'),
    path('addColaboradores', addColaboradores, name='addColaboradores'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('listado', listado, name='listado'),
<<<<<<< HEAD
    path('eliminar', eliminar, name='eliminar'),
    path('modifiColab', modifiColab, name='modifiColab'),
=======
    path('eliminar/<id>', eliminar, name='eliminar'),
    path('modificarusuario/<id>', modificarusuario, name='modificarusuario')
>>>>>>> 3261b2f21c86c2b906c5ad741b69e66d34230155
]