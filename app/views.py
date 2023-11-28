from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
import requests
import json
from django.http import JsonResponse
from datetime import datetime
from django.core.mail import send_mail

# Create your views here.

def inicio(request):
    
    
    return render(request, 'index.html')

def addColaboradores(request):
    api_url = 'https://apiarquitectura.lusaezd.repl.co/api/usuarios/add'
    
    if request.method == 'POST':
        # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        usuario_data = {
            "rut_usuario": str(request.POST.get('Rut')),
            "nombre_usuario": str(request.POST.get('NombreApellido')),
            "id_tipo": int(request.POST.get('Tipo')),
            "password": str(request.POST.get('Password')),
            "id_especialidad": int(request.POST.get('Espe'))
        }
        
        data_json = json.dumps(usuario_data)
        
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
                messages.success(request,'No se pudo crear el usuario en la API de Flask')
            
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


def modificarusuario(request):
    
    
    return render(request, 'modificar_usuario.html')

def modifiColab(request):
    
    
    return render(request, 'modificacion-cola.html', {'usuario':usuario})


def eliminar(request):
        
    return render(request, 'eliminar.html')


def tomaFecha(request):
    api_url = 'https://centromedico.aldarroyo.repl.co/api/horario-medico/fecha'
    
    usuario_data = request.session.get('usuario_data', {})
    print(usuario_data)
    if request.method == 'POST':

        fecha = request.POST.get('date')
        especialidad = request.POST.get('Espe')
        
        
        return redirect(to=f"toma-horario/{fecha}/{especialidad}")
        
    return render(request, 'toma-fecha.html')

def tomaHorario(request):
    
    return render(request, 'toma-horario.html')

def registrohorario(request):
            
    return render(request, 'registro-horario.html')





def listadoHorarioMedico(request):
    
    return render(request, 'listado-horarios.html')



def confirmaciontoma(request):
    
    return render(request, 'confirmacion-toma.html')

def resumen(request): 
    
    return render(request, 'resumen.html')

def horario(request):
    
    
    
    return render(request, 'horario.html')

def buscarAtencion(request):
    
    
    return render(request , 'buscar-atencion.html')


def eliminarhorario(request):
    return render(request, 'eliminar-horario.html')
