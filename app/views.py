from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
import requests
import json
from django.http import JsonResponse

# Create your views here.

def inicio(request):
    return render(request, 'index.html')

def addColaboradores(request):
    api_url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/add'
    
    if request.method == 'POST':
        # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        usuario_data = {
            "rut_usuario": str(request.POST.get('Rut')),
            "nombre_usuario": str(request.POST.get('NombreApellido')),
            "tipo_usuario": int(request.POST.get('Tipo')),
            "password_usuario": str(request.POST.get('Password')),
            "id_especialidad": int(request.POST.get('Espe'))
        }
        
        data_json = json.dumps(usuario_data)
        
        headers = {'Content-Type': 'application/json'}
        try:
            # Realizar una solicitud POST a la API de Flask para crear un usuario
            response = requests.post(api_url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()

                if respuesta.get("message") :
                    print("No se registro el usuario")
                    messages.warning(request, "No se registro el colaborador")
                else:
                    print(respuesta)
                    messages.success(request, "Se registro el  colaborador: " + respuesta.get("nombre"))
                print(response)

            else:
                # Manejar errores si la solicitud no fue exitosa
                return JsonResponse({'error': 'No se pudo crear el usuario en la API de Flask'}, status=500)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Error de conexión a la API de Flask'}, status=500)
        
    return render(request, 'colaboradores.html')

def login(request):
    api_url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/login'
    
    if request.method == 'POST':
        # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        usuario_data = {
            "rut_usuario": str(request.POST.get('Rut')),
            "password_usuario": str(request.POST.get('Password')),
        }
        
        data_json = json.dumps(usuario_data)
        
        headers = {'Content-Type': 'application/json'}
        try:
            # Realizar una solicitud POST a la API de Flask para crear un usuario
            response = requests.post(api_url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()

                if respuesta.get("message") :
                    print("No inicio sesion")
                    messages.warning(request, "No inicio sesion")
                else:
                    print("SI JALAAAAAAA")
                    messages.success(request, "El usuario: " + respuesta.get("nombre") + " inicio sesion")
                    return redirect(to="inicio")
                    
                    
                
                # El usuario ha sido creado exitosamente
                print(respuesta)
                # return redirect('inicio',usuario)


        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Error de conexión a la API de Flask'}, status=500)
    
    
    return render(request, 'login.html')

def register(request):
    api_url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/add'
    
    if request.method == 'POST':
        # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        usuario_data = {
            "rut_usuario": str(request.POST.get('Rut')),
            "nombre_usuario": str(request.POST.get('Nombre')),
            "tipo_usuario": 3,
            "password_usuario": str(request.POST.get('Password')),
        }
        
        data_json = json.dumps(usuario_data)
        
        headers = {'Content-Type': 'application/json'}
        try:
            # Realizar una solicitud POST a la API de Flask para crear un usuario
            response = requests.post(api_url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()

                if respuesta.get("message") :
                    print("No se registro el usuario")
                    messages.warning(request, "No se registro el usuario")
                else:
                    print(respuesta)
                    messages.success(request, "Se registro el  usuario: " + respuesta.get("nombre"))
            else:
                # Manejar errores si la solicitud no fue exitosa
                return JsonResponse({'error': 'No se pudo crear el usuario en la API de Flask'}, status=500)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Error de conexión a la API de Flask'}, status=500)
        
        
    return render(request, 'register.html')