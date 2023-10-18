from django.shortcuts import render
from django.http import HttpResponseRedirect
import requests
import json
from django.http import JsonResponse

# Create your views here.

def inicio(request):
    return render(request, 'index.html')

def addColaboradores(request):
    return render(request, 'colaboradores.html')

def login(request):
    
    
    
    return render(request, 'login.html')

def register(request):
    api_url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/add'
    
    if request.method == 'POST':
        # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        usuario_data = {
            "rut_usuario": str(request.POST.get('rut')),
            "nombre_usuario": str(request.POST.get('nombre')),
            "tipo_usuario": int(request.POST.get('tipo_usuario')),
            "password_usuario": str(request.POST.get('password'))
        }
        
        data_json = json.dumps(usuario_data)
        
        headers = {'Content-Type': 'application/json'}
        try:
            # Realizar una solicitud POST a la API de Flask para crear un usuario
            response = requests.post(api_url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                mensaje = response.json()
                # El usuario ha sido creado exitosamente
                print(mensaje)
                #return JsonResponse({'mensaje': 'Usuario creado exitosamente'}, status=200)
            else:
                # Manejar errores si la solicitud no fue exitosa
                return JsonResponse({'error': 'No se pudo crear el usuario en la API de Flask'}, status=500)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Error de conexión a la API de Flask'}, status=500)
        
        
    return render(request, 'register.html')