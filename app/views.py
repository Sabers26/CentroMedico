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
    api_url = 'https://centromedico.aldarroyo.repl.co/api/usuarios/add'
    
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
    api_url = 'https://centromedico.aldarroyo.repl.co/api/usuarios/login'
    
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
                    request.session['usuario_data'] = usuario_data
                    messages.success(request, "El usuario: " + respuesta.get("nombre") + " inicio sesion")
                    return redirect(to="inicio")
                    
                    
                
                # El usuario ha sido creado exitosamente
                print(respuesta)
                # return redirect('inicio',usuario)


        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': 'Error de conexión a la API de Flask'}, status=500)
    
    
    return render(request, 'login.html')

def register(request):
    api_url = 'https://centromedico.aldarroyo.repl.co/api/usuarios/add'
    
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
        api_url = 'https://centromedico.aldarroyo.repl.co/api/usuarios'
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
            
            response = requests.post('https://centromedico.aldarroyo.repl.co/api/usuarios/tipo', data=data_json, headers=headers)
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
            
            response = requests.post('https://centromedico.aldarroyo.repl.co/api/usuarios/especialidad', data=data_json, headers=headers)
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
            
            response = requests.post('https://centromedico.aldarroyo.repl.co/api/usuarios/buscarUsuario', data=data_json, headers=headers)
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
    api_url = 'https://centromedico.aldarroyo.repl.co/api/usuarios/buscarUsuario'
    
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
            url = 'https://centromedico.aldarroyo.repl.co/api/usuarios/mod'
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
        api_url = 'https://centromedico.aldarroyo.repl.co/api/usuarios/buscarUsuario'
        
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

            
            url = 'https://centromedico.aldarroyo.repl.co/api/usuarios/mod'
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
            url = 'https://centromedico.aldarroyo.repl.co/api/usuarios/act'
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


def tomaFecha(request):
    api_url = 'https://centromedico.aldarroyo.repl.co/api/horario-medico/fecha'
    
    usuario_data = request.session.get('usuario_data', {})
    print(usuario_data)
    if request.method == 'POST':

        fecha = request.POST.get('date')
        especialidad = request.POST.get('Espe')
        
        
        return redirect(to=f"toma-horario/{fecha}/{especialidad}")
        
    return render(request, 'toma-fecha.html')

def tomaHorario(request, fecha, especialidad):
    
    lista = []
    
    api_url = 'https://centromedico.aldarroyo.repl.co/api/horario-medico/fecha'
    
    respuesta = None  # Inicializa la variable respuesta antes del bloque try
    
    fecha_original = fecha

    # # Convierte la fecha en un objeto datetime
    fecha_obj = datetime.strptime(fecha_original, '%Y-%m-%d')

    # # Formatea la fecha en 'DD-MM-YYYY'
    fecha_formateada = fecha_obj.strftime('%d-%m-%Y')   
    
    data ={
        "fecha": fecha_formateada,
        "especialidad_id": int(especialidad)
    }
    
    if 'usuario_data' in request.session:
        # Accede al diccionario almacenado en la sesión
        usuario_data = request.session['usuario_data']

        # Recupera el valor de 'rut_usuario'
        rut_usuario = usuario_data.get('rut_usuario', None)
    
    
    
    if request.method == 'GET':
        data_json = json.dumps(data)
        
        headers = {'Content-Type': 'application/json'}
        try:
            # Realizar una solicitud POST a la API de Flask para crear un usuario
            response = requests.post(api_url, data=data_json, headers=headers)
            if response.status_code == 200:
                respuesta = response.json()
                if len(respuesta)==0:
                    messages.warning(request, "No se encontraron horas")
                else:
                    print("LLEGE AL ELSE")
                    lista = []
                    for item in respuesta:
                        # Crear una lista de horarios médicos para el elemento actual
                        horarios = item['horario_medico']

                        for horario in horarios:
                            lista.append({
                                'fecha': horario['fecha'],
                                'hora_bloque': horario['horario']['hora_bloque'],
                                'id_bloque': horario['horario']['id'],
                                'nombre': item['nombre'],
                                'rut': item['rut'],
                                'rut_paciente': rut_usuario
                            })
                            print(lista)
                            
                    if len(lista)==0:
                        messages.warning(request, "No se encontraron horas")

                    # Ordenar la lista de datos en orden descendente por la hora del bloque
                    lista = sorted(lista, key=lambda x: datetime.strptime(x['hora_bloque'], '%H:%M'), reverse=False)
                    print("SI JALAAAAAAA")
                    #messages.success(request, "El usuario: " + respuesta.get("nombre") + " inicio sesión")
                    #request.session['usuario_data'] = usuario_data
                
        except Exception as e:
            messages.warning(request, f"Error con el servidor: {str(e)}")
            print("me cai:", str(e))
                
    return render(request, 'toma-horario.html', {'lista': lista})

def registrohorario(request,id):
    api_url = 'https://centromedico.aldarroyo.repl.co/api/horario-medico/add'
    
    # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        
    lista_horas = []
    if request.method == 'POST':
        #Obtiene el rango de fecha
        rango_fecha = request.POST.get('daterange')
        
        #Separa las fechas y las almacena en 2 variables
        fechas_separadas = rango_fecha.split(" - ")
        fecha_inicio = fechas_separadas[0]
        fecha_fin = fechas_separadas[1]
        
        #Esto es para darle el formato adecuado en la base de datos
        fecha_inicio = datetime.strptime(fecha_inicio, "%m/%d/%Y").strftime("%Y-%m-%d")
        fecha_fin = datetime.strptime(fecha_fin, "%m/%d/%Y").strftime("%Y-%m-%d")

        
        print(fecha_inicio)
        
        #Obtiene todas los horarios seleccionados
        valores_checkbox = request.POST.getlist('hora')
        for valor in valores_checkbox:
            lista_horas.append(valor)

            
        solicitud = {
            "rut_usuario": id,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "horarios": lista_horas
        }
        
        data_json = json.dumps(solicitud)
        
        headers = {'Content-Type': 'application/json'}
        try:
            response = requests.post(api_url, data=data_json, headers=headers)
            # Comprobar si la solicitud fue exitosa (código de estado 200 para indicar que la api retorna informacion)
            if response.status_code == 200:
                respuesta = response.json()
                if respuesta.get("message"):
                    messages.warning(request, "No se registraron las horas del medico")
                    return redirect(to="listado")
                elif respuesta.get("filas"):
                    messages.success(request, "Horas registradas correctamente")
                    return redirect(to="listado")
                else:
                    messages.success(request, "No se pudo realizar la acción")
                    return redirect(to="listado")
                    
        except:
            messages.warning(request,'Error de conexión a la API de Flask')
            return redirect(to="inicio")
            
    return render(request, 'registro-horario.html')





def listadoHorarioMedico(request, id):
    try:
        api_url = "https://centromedico.aldarroyo.repl.co/api/horario-medico/buscar"
        
        usuario_data = {
            "rut_usuario": id
        }
        headers = {'Content-Type': 'application/json'}
        
        data_json = json.dumps(usuario_data)
        
        response = requests.post(api_url, data=data_json, headers=headers)
        datos = None
        
        # Comprobar si la API responde con éxito (código 200)
        if response.status_code == 200:
            datos = response.json()
            if "message" in datos:
                messages.warning(request, 'No se encontraron horarios')
            else:
                messages.warning(request, 'No se encontraron horarios')
        else:
            messages.error(request, 'Error al obtener datos de la API')
            
    except Exception as e:
        messages.error(request, f'Error del servidor: {str(e)}')
    
    return render(request, 'listado-horarios.html', {'datos': datos})



def confirmaciontoma(request,data):
    api_url = "https://centromedico.aldarroyo.repl.co/api/atenciones/add"
    
    # Reemplaza comillas simples por comillas dobles en la cadena JSON
    data = data.replace("'", '"')

    data = json.loads(data)  # Convierte la cadena JSON en un diccionario

    api_url = "https://centromedico.aldarroyo.repl.co/api/atenciones/add"

    atencion = {
        "fecha_consulta": data['fecha'],
        "rut_medico": data['rut'],
        "hora_consulta": data['id_bloque'],
        "rut_paciente": data['rut_paciente'].replace("-", "")
    }
    
    if request.method == 'POST':
        data_json = json.dumps(atencion)
        
        correo = str(request.POST.get('correo'))
    
        
        # Convierte el objeto JSON en un diccionario de Python
        
        headers = {'Content-Type': 'application/json'}
        try:
            # Realizar una solicitud POST a la API de Flask para crear un usuario
            response = requests.post(api_url, data=data_json, headers=headers)

            # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
            if response.status_code == 200:
                respuesta = response.json()
                if respuesta.get("message") :
                    messages.warning(request, "No se registro el usuario")
                    
                else:
                    print("JALOOO")
                    
                    
                    
                    # Genera la URL con el objeto JSON directamente en la URL
                    url_destino = f'/resumen/{respuesta}'
                    
                    send_mail(
                        'Reserva hora centro medico',
                        'Hora confirmada.',
                        'apicorreosduoc@gmail.com',
                        [correo],
                        fail_silently=False,
                        )
                    
                    return redirect(url_destino)
                    
                    
            else:
                messages.warning(request,'No se pudo crear la atencion en la API de Flask')
                
        except:
            messages.warning(request,'Error de conexión a la API de Flask')
    

    
    
    
    return render(request, 'confirmacion-toma.html')

def resumen(request,data):
    print("DATA VISTA RESUMEN: ",data)
    
    data = data.replace("'", '"')

    data = json.loads(data)  # Convierte la cadena JSON en un diccionario
    
    
    
    
    return render(request, 'resumen.html', {"data": data})

def horario(request):
    
    
    
    return render(request, 'horario.html')

def buscarAtencion(request):
    
    
    
    return render(request , 'buscar-atencion.html')


    