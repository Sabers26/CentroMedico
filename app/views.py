from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import requests
import json
from django.http import JsonResponse
from datetime import datetime
from django.core.mail import send_mail
from urllib.parse import unquote

# Create your views here.

def inicio(request):
    
    
    return render(request, 'index.html')

def addColaboradores(request):
    api_url = 'https://apiarquitectura.lusaezd.repl.co/api/usuarios/add'
    
    if request.method == 'POST':
        # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        usuario_data = {
            "rut_usuario": str(request.POST.get('rut')),
            "nombre_usuario": str(request.POST.get('nombreApellido')),
            "id_tipo": int(request.POST.get('tipo')),
            "password": str(request.POST.get('password')),
            "id_especialidad": int(request.POST.get('espe'))
        }
        
        data_json = json.dumps(usuario_data)
        
        print(usuario_data)
        
        headers = {'Content-Type': 'application/json'}
        
        try:
            response = requests.post(api_url, data=data_json, headers=headers)
            print("vacio")
            
            if response.status_code == 200:
                print("Obtuve respusta api")
                respuesta = response.json()
                
                print("RESPUESTA")
                print(respuesta)
                
                if respuesta.get("correcto") :
                    print("Si se pudo")
                    messages.success(request, respuesta["correcto"])
                    return redirect(to="listado")
                else:
                    print("No se pudo")
                    messages.warning(request, "No se registro el colaborador")
                    return redirect(to="listado")
            else:
                # Manejar errores si la solicitud no fue exitosa
                messages.success(request,'Error en la respuesta de la API de Flask')
            
        except requests.exceptions.RequestException:
            messages.success(request,'Error de conexión a la API de Flask')
            return redirect(to="listado")
        
    
    return render(request, 'admin/colaboradores.html')

def login(request):
    
    return render(request, 'login.html')

def register(request):
        
        
    return render(request, 'register.html')


def listado(request):
    return render(request, 'admin/listado.html')


def modificarusuario(request, rut, tipo):
    try:
        if request.method == 'POST':


            especialidad = request.POST.get('espe')
            
            if especialidad == "":
                especialidad = None
                
            usuario_data = {
                "rut_usuario": rut,
                "nombre_usuario": str(request.POST.get('nombre')),
                "password": str(request.POST.get('password')),
                "id_especialidad": especialidad
            }
            
            print("===================================")
            print(usuario_data)
            
            data_json = json.dumps(usuario_data)
            

            headers = {'Content-Type': 'application/json'}

            
            url = 'https://apiarquitectura.lusaezd.repl.co/api/usuarios/mod'
            # Realizar una solicitud POST a la API de Flask para modificar un usuario
            response = requests.post(url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()

                if respuesta.get("correcto") == "Usuario modificado correctamente!":
                    print(respuesta)
                    messages.success(request, "Se modifico el  usuario rut: " + str(rut))
                    return redirect(to="listado")
                else:
                    print("No se modifico el usuario")
                    print(respuesta)
                    messages.warning(request, "No se modifico el usuario")
                    return redirect(to="listado")
                
            else:
                # Manejar errores si la solicitud no fue exitosa
                messages.warning(request, 'Error en la respuesta de la API de Flask')
                return redirect(to="listado")
            
    except requests.exceptions.RequestException:
        messages.warning(request,'Error de conexión a la API de Flask')
        return redirect(to="listado")
    
    usuario = {
        "rut_usuario": rut,
        "id_tipo": tipo
    }
    return render(request, 'admin/modificar_usuario.html', {'usuario': usuario})

def eliminar(request,rut,estado):
    usuario_data = {
        "rut_usuario": str(rut),
        "estado": estado
    }
    data_json = json.dumps(usuario_data)
    
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        url = 'https://apiarquitectura.lusaezd.repl.co/api/usuarios/modEstado'
        # Realizar una solicitud POST a la API de Flask para deshabilitar el usuario
        response = requests.post(url, data=data_json, headers=headers)

        # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
        if response.status_code == 200:
            respuesta = response.json()
            print("RESPUESTA==============")
            print(respuesta)

            if respuesta.get("correcto") == "Se ha modificado el estado del usuario correctamente!":
                messages.success(request, "Se ha modificado el estado del  usuario")
            else:
                messages.warning(request, "No se ha modificado el estado del  usuario")
        else:
            # Manejar errores si la solicitud no fue exitosa
            messages.warning(request,'Error en la respuesta de la API de Flask')

    except requests.exceptions.RequestException:
        messages.warning(request,'Error de conexión a la API de Flask')
    return redirect(to="listado")


def tomaFecha(request):
    
    return render(request, 'user/toma-fecha.html')

def tomaHorario(request):
    
    return render(request, 'user/toma-horario.html')

def registrohorario(request):
            
    return render(request, 'admin/registro-horario.html')





def listadoHorarioMedico(request):
    
    return render(request, 'admin/listado-horarios.html')



def confirmaciontoma(request):
    
    return render(request, 'user/confirmacion-toma.html')

def resumen(request): 
    
    return render(request, 'user/resumen.html')

def horario(request):
    
    
    
    return render(request, 'horario.html')

def buscarAtencion(request):
    
    
    return render(request , 'admin/buscar-atencion.html')


def eliminarhorario(request):
    return render(request, 'eliminar-horario.html')



def lista_usuarios(_request):
    api_url = 'https://apiarquitectura.lusaezd.repl.co/api/usuarios/'
    response = requests.get(api_url)
    
    # Verificar si la respuesta fue exitosa (código 200)
    if response.status_code == 200:
        # Convertir la respuesta a una lista de diccionarios
        usuarios = response.json()
        return JsonResponse(usuarios, safe=False)
    else:
        # Manejar el caso en que la respuesta no sea exitosa
        return JsonResponse({'error': 'No se pudo obtener la lista de usuarios'}, status=response.status_code)
