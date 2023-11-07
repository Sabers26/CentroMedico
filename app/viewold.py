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
        
        
        if int(request.POST.get('Tipo')) == 1:
            del usuario_data["id_especialidad"]

        
        data_json = json.dumps(usuario_data)
        
        headers = {'Content-Type': 'application/json'}
        try:
            # Realizar una solicitud POST a la API de Flask para crear un usuario
            response = requests.post(api_url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()

                if respuesta.get("message") :
                    messages.warning(request, "No se registro el colaborador")
                    return redirect(to="listado")
                else:
                    messages.success(request, "Se registro el  colaborador: " + respuesta.get("nombre"))
                    return redirect(to="listado")

            else:
                # Manejar errores si la solicitud no fue exitosa
                messages.success(request,'No se pudo crear el usuario en la API de Flask')
        except requests.exceptions.RequestException:
            messages.success(request,'Error de conexión a la API de Flask')
            return redirect(to="listado")
        
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
                    messages.warning(request, "No se registro el usuario")
                    return redirect(to="inicio")
                else:
                    messages.success(request, "Se registro el  usuario: " + respuesta.get("nombre"))
                    return redirect(to="inicio")
            else:
                # Manejar errores si la solicitud no fue exitosa
                messages.warning(request,'No se pudo crear el usuario en la API de Flask')
                return redirect(to="inicio")
            
        except requests.exceptions.RequestException:
            messages.warning(request,'Error de conexión a la API de Flask')
            return redirect(to="inicio")
        
        
    return render(request, 'register.html')


def listado(request):
    try:
        api_url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios'
        response = requests.get(api_url)
        usuarios = None
        # Comprobar si la api da respuesta
        if response.status_code == 200:
            usuarios = response.json()
            if "message" in usuarios:
                messages.warning(request,'No se encontraron usuarios')
            
            
            
        

        # Obtén los valores de los campos de filtro del formulario
        tipo_usuario = request.GET.get('tipoUsuario')
        id_especialidad = request.GET.get('idEspecialidad')
        rut = request.GET.get('Rut')
        usuariob = None #Esto limpia a usuario busqueda del diccionario de datos

        # Si obtiene algun elemento del filtro como tipo o especialidad llama al metodo de la API para filtrar
        if tipo_usuario:
            usuario_data = {
                "tipo_usuario": tipo_usuario
            }
            
            data_json = json.dumps(usuario_data)
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post('https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/tipo', data=data_json, headers=headers)
            if response.status_code == 200:
                usuarios = response.json()
                if "message" in usuarios:
                    messages.warning(request,'No se encontraron usuarios filtrados por tipo')
        
        if id_especialidad:
            usuario_data = {
                "id_especialidad": id_especialidad
            }
            
            data_json = json.dumps(usuario_data)
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post('https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/especialidad', data=data_json, headers=headers)
            if response.status_code == 200:
                usuarios = response.json()
                if "message" in usuarios:
                    messages.warning(request,'No se encontraron usuarios filtrados por especialidad')
        if rut:
            
            # Le añade el guion al rut para que la api no lo rechace por las validaciones
            # rut_con_guion = rut[:-1] + "-" + rut[-1]
            # print(rut_con_guion)
            usuario_data = {
                "rut_usuario": rut
            }
            
            data_json = json.dumps(usuario_data)
            headers = {'Content-Type': 'application/json'}
            
            response = requests.post('https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/buscarUsuario', data=data_json, headers=headers)
            if response.status_code == 200:
                usuariob = response.json()
                if "message" in usuariob:
                    print(usuariob)
                    usuariob = None
                    messages.warning(request,'No se encontraron usuarios filtrados por tipo')
            usuarios = None #Al buscar por rut esto limpia a los usuarios del diccionario de datos
                
                
        diccionario = { #El diccionario esta para enviar a los usuarios o a un usuario de la busqueda
        'usuarios': usuarios,
        'usuariob':usuariob
        }

        if usuariob:
            diccionario['usuariob'] = usuariob

        return render(request, 'listado.html', {'diccionario': diccionario})
    except requests.exceptions.RequestException:
        return  messages.warning(request,'Error de conexión a la API de Flask')




def modificarusuario(request,id):
    #Primero obtener el usuario para que sus datos se muestren en el formulario
    api_url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/buscarUsuario'
    
    usuario_rut = {
        "rut_usuario": str(id),
    }
        
    data_json = json.dumps(usuario_rut)
    
    headers = {'Content-Type': 'application/json'}

    response = requests.post(api_url, data=data_json, headers=headers)
    usuario = response.json()
    
    
    
    if request.method == 'POST':
        rut = str(request.POST.get('Rut'))
        rut_con_guion = rut[:-1] + "-" + rut[-1]

        usuario_data = {
            "rut_usuario": rut_con_guion,
            "nombre_usuario": str(request.POST.get('NombreApellido')),
            "password_usuario": str(request.POST.get('Password')),
        }
        
        data_json = json.dumps(usuario_data)
        
        headers = {'Content-Type': 'application/json'}

        try:
            url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/mod'
            # Realizar una solicitud POST a la API de Flask para crear un usuario
            response = requests.post(url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()

                if respuesta.get("message") == "Usuario modificado correctamente":
                    print(respuesta)
                    messages.success(request, "Se modifico el  usuario: ")
                    return redirect(to="listado")
                else:
                    messages.warning(request, "No se modifico el usuario")
                    return redirect(to="listado")
                
            else:
                # Manejar errores si la solicitud no fue exitosa
                return messages.warning(request, 'No se pudo modificar el usuario en la API de Flask')
        except requests.exceptions.RequestException:
            return  messages.warning(request,'Error de conexión a la API de Flask')

    
    return render(request, 'modificar_usuario.html',{'usuario': usuario})

def modifiColab(request,id):
    try:
        #Primero obtener el usuario para que sus datos se muestren en el formulario
        api_url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/buscarUsuario'
        
        usuario_rut = {
            "rut_usuario": str(id),
        }
            
        data_json = json.dumps(usuario_rut)
        
        headers = {'Content-Type': 'application/json'}

        response = requests.post(api_url, data=data_json, headers=headers)
        
        if response.status_code == 200:
            usuario = response.json()
            if "message" in usuario:
                messages.warning(request, "Usuario no encontrado en la base de datos")
                return redirect(to="listado")
        
        
        if request.method == 'POST':
            rut = str(id)
            # rut_con_guion = rut[:-1] + "-" + rut[-1]

            especialidad = request.POST.get('idEspecialidad')
            
            if especialidad == "":
                especialidad = None
                
            # if especialidad is None:
            #     especialidad = None  # O cualquier otra acción que desees realizar
            
            usuario_data = {
                "rut_usuario": rut,
                "nombre_usuario": str(request.POST.get('Nombre')),
                "password_usuario": str(request.POST.get('Password')),
                "id_especialidad": especialidad
            }
            
            data_json = json.dumps(usuario_data)
            

            headers = {'Content-Type': 'application/json'}

            
            url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/mod'
            # Realizar una solicitud POST a la API de Flask para modificar un usuario
            response = requests.post(url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()

                if respuesta.get("message") == "Usuario modificado correctamente":
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
                messages.warning(request, 'No se pudo modificar el usuario en la API de Flask')
                return redirect(to="listado")
            
    except requests.exceptions.RequestException:
        messages.warning(request,'Error de conexión a la API de Flask')
        return redirect(to="listado")
    
    return render(request, 'modificacion-cola.html', {'usuario':usuario})


def eliminar(request,id,estado):
    if request.method == 'POST':
        usuario_data = {
            "rut_usuario": str(id),
        }
        data_json = json.dumps(usuario_data)
        
        print(data_json)
        
        headers = {'Content-Type': 'application/json'}
        
        try:
            url = 'https://centromedicoarquitectura.lusaezd.repl.co/api/usuarios/act'
            # Realizar una solicitud POST a la API de Flask para deshabilitar el usuario
            response = requests.post(url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()

                if respuesta.get("message") == "Se modifico al usuario correctamenete":
                    print(respuesta)
                    if estado == 'HABILITADO':
                        messages.success(request, "Se deshabilito el  usuario")
                    elif estado == 'DESHABILITADO':
                        messages.success(request, "Se habilito el  usuario")
                    return redirect(to="listado")
                else:
                    messages.warning(request, "No se modifico el usuario")
                    return redirect(to="listado")
                
            else:
                # Manejar errores si la solicitud no fue exitosa
                messages.warning(request,'No se pudo modificar el usuario en la API de Flask')
                return redirect(to="listado")
                
        except requests.exceptions.RequestException:
            messages.warning(request,'Error de conexión a la API de Flask')
            return redirect(to="listado")
        
        
    
    return render(request, 'eliminar.html', {'id': id, 'estado': estado})

