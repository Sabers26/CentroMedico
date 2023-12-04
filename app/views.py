from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
import requests
import json
from django.http import JsonResponse
from datetime import datetime
from django.core.mail import send_mail
from urllib.parse import unquote
import openpyxl
from django.urls import reverse

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
                
                if "correcto" in respuesta :
                    print("Si se pudo")
                    messages.success(request, "Se registro al usuario rut: "+ str(request.POST.get('rut')))
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
    api_url = 'https://apiarquitectura.lusaezd.repl.co/api/usuarios/login'
    
    if request.method == 'POST':
        # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        usuario_data = {
            "rut_usuario": str(request.POST.get('rut')),
            "password": str(request.POST.get('password')),
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
                    messages.warning(request, "Usuario y/o contraseña incorrectos")
                    print(respuesta)
                else:
                    request.session['usuario_data'] = usuario_data
                    messages.success(request, "El usuario " + respuesta.get("nombre_usuario") + " inicio sesion")
                    return redirect(to="inicio")
                    
            else:
                # Manejar errores si la solicitud no fue exitosa
                messages.success(request,'Error en la respuesta de la API de Flask')
                return redirect(to="inicio")

        except requests.exceptions.RequestException as e:
            messages.warning('Error de conexión a la API de Flask')
            return redirect(to="inicio")
    return render(request, 'login.html')

def register(request):
    api_url = 'https://apiarquitectura.lusaezd.repl.co/api/usuarios/add'
    
    if request.method == 'POST':
        # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
        usuario_data = {
            "rut_usuario": str(request.POST.get('rut')),
            "nombre_usuario": str(request.POST.get('nombreApellido')),
            "id_tipo": 3,
            "password": str(request.POST.get('password')),
            "id_especialidad": None
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
                
                if "correcto" in respuesta :
                    print("Si se pudo")
                    messages.success(request, "Se registro al usuario rut: "+ str(request.POST.get('rut')))
                    return redirect(to="inicio")
                else:
                    print("No se pudo")
                    messages.warning(request, "No se registro el colaborador")
                    return redirect(to="inicio")
            else:
                # Manejar errores si la solicitud no fue exitosa
                messages.success(request,'Error en la respuesta de la API de Flask')
            
        except requests.exceptions.RequestException:
            messages.success(request,'Error de conexión a la API de Flask')
            return redirect(to="inicio")
        
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
    if request.method == 'POST':
        
        if 'usuario_data' in request.session:
            # Accede al diccionario almacenado en la sesión
            usuario_data = request.session['usuario_data']

            # Recupera el valor de 'rut_usuario'
            rut_usuario = usuario_data.get('rut_usuario', None)
        else:
            messages.warning(request,"Debe iniciar sesion para poder ver horarios.")
            return redirect(to="login")
        
        
        fecha = request.POST.get('dia')
        id_especialidad = request.POST.get('Espe')
        
        if not fecha:
            messages.warning(request,"Debe ingresar la fecha.")
            
        if id_especialidad == "0":
            messages.warning(request, "Debe seleccionar una el especialidad.")
            
        if fecha and id_especialidad != "0":
            usuario_data = {
                "fecha": fecha,
                "id_especialidad": id_especialidad,
            }
            return redirect(to="tomahorario/"+fecha+"/"+id_especialidad+"/"+rut_usuario)

    return render(request, 'user/toma-fecha.html')

def tomaHorario(request, fecha, especialidad, rut):
    # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
    usuario_data = {
        "fecha": fecha,
        "id_especialidad": especialidad,
    }
    
    print(fecha)
    
    
    data_json = json.dumps(usuario_data)
    
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post("https://apiarquitectura.lusaezd.repl.co/api/horarioMedico/buscarEsp", data=data_json, headers=headers)
        data = response.json()
        
        context = {
            "data": data,
            "rut_paciente": rut.replace("-", "")
        }
        
        if response.status_code == 200:
                respuesta = response.json()
                if isinstance(respuesta, list):
                    print(respuesta)
                    print("Hubo respuesta")
                    if len(respuesta) > 0:
                        print("si se encontraron datos")
                        print(respuesta)
                        return render(request, 'user/toma-horario.html', {'context': context})
                    else:
                        messages.warning(request, "No se encontraron horarios para el dia indicado")
                        print("no se encontraron horarios")
                        return redirect(to="toma-fecha")
                else:
                    print("Error al obtener horas por especialidad")
                    messages.warning(request, "No error al obtener horarios")
                    print(respuesta)
                    return redirect(to="toma-fecha")
        else:
            messages.warning(request, "ERROR API")
            print(respuesta)
            return redirect(to="toma-fecha")
    except Exception as ex:
        print("EXCEPCION: ",ex)
        return redirect(to="toma-fecha")


def atencion (request, rut_medico,rut_paciente, fecha, id_horario, correo):
    
    rut_medico = agregar_guin_a_rut(rut_medico)
    
    rut_paciente = agregar_guin_a_rut(rut_paciente)
    
    usuario_data ={
        "rut_medico": rut_medico,
        "rut_paciente": rut_paciente,
        "fecha": fecha,
        "id_horario": id_horario
    }
    
    data_json = json.dumps(usuario_data)
    
    print(data_json)
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        url = 'https://apiarquitectura.lusaezd.repl.co/api/atenciones/add'
        # Realizar una solicitud POST a la API de Flask para deshabilitar el usuario
        response = requests.post(url, data=data_json, headers=headers)

        # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
        if response.status_code == 200:
            respuesta = response.json()
            print("RESPUESTA==============")
            print(respuesta)
            print(rut_paciente)

            if respuesta.get("correcto") == "Atencion agregada correctamente":
                send_mail(
                        'Reserva hora centro medico',
                        'Hora confirmada.',
                        'apicorreosduoc@gmail.com',
                        [correo],
                        fail_silently=False,
                        )
                messages.success(request, "Atencion agregada correctamente")
                
                url_resumen = reverse('resumen', kwargs={'rut_medico': rut_medico, 'rut_paciente': rut_paciente, 'fecha': fecha, 'id_horario': id_horario})
                return redirect(url_resumen)
            else:
                messages.warning(request, "No se pudo tomar la atencion")
        else:
            # Manejar errores si la solicitud no fue exitosa
            messages.warning(request,'Error en la respuesta de la API de Flask')

    except requests.exceptions.RequestException:
        messages.warning(request,'Error de conexión a la API de Flask')
    return redirect(to="toma-fecha")

def resumen(request, rut_medico, rut_paciente, fecha, id_horario):
    horario = ["8:00","9:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00"]
    print("LLEGUE AL RESUMEN")
    print("RUT_MEDICO: ", rut_medico)
    print("HORA", id_horario)
    hora = horario[int(id_horario)-1]
    

    # ... tu código existente ...
    return render(request, 'user/resumen.html', {'rut_medico': rut_medico, 'rut_paciente': rut_paciente, 'fecha': fecha, 'hora': hora})


def lista_atenciones(request,rut):
    usuario_data = {
        "rut_usuario": str(rut),
    }
    
    
    
    rutoriginal = rut
    
    data_json = json.dumps(usuario_data)
    
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post("https://apiarquitectura.lusaezd.repl.co/api/atenciones/buscar", data=data_json, headers=headers)
        data = response.json()
        
        context= {
            'datos_usuarios':data,
            'rut': rutoriginal,
            'rutsin': rut.replace("-", "")
        }
        
        if response.status_code == 200:
                respuesta = response.json()
                if isinstance(respuesta, list):
                    return render(request, 'user/listado-atenciones.html', {'context': context})
                elif respuesta.get("message") == "No hay atenciones asociadas al paciente":
                    context['datos_usuarios'] = []
                    print("No hay horas atenciones asociadas a este paciente")
                    return render(request, 'user/listado-atenciones.html', {'context': context})
                else:
                    print("No error al obtener atenciones")
                    messages.warning(request, "Error al obtener las atenciones")
                    return redirect(to="listado")
        else:
            messages.warning(request, "ERROR API")
            print(respuesta)
            return redirect(to="listado")
    except Exception as ex:
        print("EXCEPCION: ",ex)
        return redirect(to="listado")

def eliminar_atencion(request, ida, rut, fecha, idh, rutpa):

    rutpa = agregar_guin_a_rut(rutpa)
    usuario_data = {
        "id_atencion": ida,
        "rut_medico": rut,
        "fecha_consulta": fecha,
        "id_horario": idh
    }
    data_json = json.dumps(usuario_data)
    
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        url = 'https://apiarquitectura.lusaezd.repl.co/api/atenciones/anular'
        # Realizar una solicitud POST a la API de Flask para deshabilitar el usuario
        response = requests.post(url, data=data_json, headers=headers)

        # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
        if response.status_code == 200:
            respuesta = response.json()
            print("RESPUESTA==============")
            print(respuesta)

            if respuesta.get("correcto") == "Se ha anulado correctamente la atencion":
                messages.success(request, "Se ha anulado la atencion")
            else:
                messages.warning(request, "No se ha anulado la atencion")
        else:
            # Manejar errores si la solicitud no fue exitosa
            messages.warning(request,'Error en la respuesta de la API de Flask')

    except requests.exceptions.RequestException:
        messages.warning(request,'Error de conexión a la API de Flask')
    return redirect(to="http://127.0.0.1:8000/lista_atenciones/"+rutpa)


def registrohorario(request,rut):
    try:
        if request.method == 'POST':
            rut_medico= rut
            
            archivo = request.FILES['archivo']
            
            archivo_excel = openpyxl.load_workbook(archivo, data_only=True)

            hoja = archivo_excel['Hoja1']
            rango_celdas = hoja['A9:G14']
            rangohoras = hoja['I9:O18']
            celdas_amarillas = {dia: [] for dia in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
            recorriendo_rango = False

            for fila in rango_celdas:
                for celda in fila:
                    valor_celda = celda.value
                    color_celda = celda.fill.fgColor.rgb if celda.fill.fgColor is not None else None

                    if isinstance(valor_celda, datetime):
                        dia_celda = valor_celda.strftime('%d')
                        mes_y_anio_celda = valor_celda.strftime('%Y-%m')
                        dia = valor_celda.strftime('%A')  # Cambiado a inglés
                            
                        if dia_celda == '01':
                            if recorriendo_rango:
                                recorriendo_rango = False
                            else:
                                recorriendo_rango = True

                        if recorriendo_rango:
                            if color_celda == 'FFFFFF00' and recorriendo_rango:
                                celdas_amarillas[dia].append(mes_y_anio_celda+'-'+dia_celda)
                                
            celdas_amarillas = [celdas_amarillas[dia] for dia in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]

            rango_celdas_transpuesto = list(zip(*rangohoras))
            horas = []

            for columna in rango_celdas_transpuesto:
                columna_lista = []
                for celda in columna:
                    if celda.fill.start_color.rgb == 'FFFFFF00':
                        valor_celda = str(celda.value)
                        columna_lista.append(valor_celda)

                horas.append(columna_lista)
            
            #Valida si tiene 
            for i in range(len(celdas_amarillas)):
                # Verificar si la lista en el mismo índice en la segunda lista está vacía
                if not horas[i]:
                    if celdas_amarillas[i] != []:
                        print( celdas_amarillas[i] )
                        print(f"Debe agregar en el día {i}")
                        messages.warning(request,"Debe agregar en el día")
                        return redirect(to="registrohorario")

            messages.success(request, "Correcto")
            
            print("Dias seleccionados:", celdas_amarillas)

            print(horas)

            archivo_excel.close()

            try:
                horario_data = {
                    "dias": f"{celdas_amarillas}",
                    "horas":f"{horas}",
                    "rut_usuario": f"{rut_medico}"
                }
                
                {
                    "dias": "[['12-06-2023', '26-06-2023'], ['27-06-2023'], ['07-06-2023'], ['15-06-2023'], ['09-06-2023'], ['24-06-2023'], []]", 
                    "horas": "[['2', '4'], ['2', '4'], ['7'], ['4'], ['7', '10'], ['5'], []]", 
                    "rut_usuario": "20749760-6"
                }
                data_json = json.dumps(horario_data)
                
                print(data_json)
                
                headers = {'Content-Type': 'application/json'}

                
                url = 'https://apiarquitectura.lusaezd.repl.co/api/horarioMedico/add'
                # Realizar una solicitud POST a la API de Flask para modificar un usuario
                response = requests.post(url, data=data_json, headers=headers)
                respuesta = response.json()
                # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
                if response.status_code == 200:
                    

                    if respuesta.get("correcto") == "Se han ingresado los horarios a la agenda del medico":
                        print(respuesta)
                        messages.success(request, "Agregaron las horas al medico: " + str(rut))
                        return redirect(to=reverse("listadoHorarioMedico", kwargs={'rut': rut_medico}))
                    else:
                        print("No se agregaron las horas")
                        print(respuesta)
                        messages.warning(request, "No Agregaron las horas al medico: " + str(rut))
                        return redirect(to=reverse("listadoHorarioMedico", kwargs={'rut': rut_medico}))
                    
                else:
                    # Manejar errores si la solicitud no fue exitosa
                    messages.warning(request, 'Error en la respuesta de la API de Flask') #Error en la respuesta de la API de Flask
                    return redirect(to=reverse("listadoHorarioMedico", kwargs={'rut': rut_medico}))
            
            except requests.exceptions.RequestException as e:
                print("ERRORRRR: ",e)
                messages.warning(request,'Error de conexión a la API de Flask')
                return redirect(to=reverse("listadoHorarioMedico", kwargs={'rut': rut_medico}))
            
            
    except Exception as e:
        messages.warning(request,'Error el procesar el archivo')
        print("Hubo un error:", str(e))
            
    return render(request, 'admin/registro-horario.html')





def listadoHorarioMedico(request,rut:str):
    # Si se envió un formulario, trae los datos del formulario y los guarda en un JSON
    usuario_data = {
        "rut": str(rut),
    }
    
    rutoriginal = rut
    
    data_json = json.dumps(usuario_data)
    
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post("https://apiarquitectura.lusaezd.repl.co/api/horarioMedico/buscar", data=data_json, headers=headers)
        data = response.json()
        
        context= {
            'datos_usuarios':data,
            'rut': rutoriginal,
            'rutsin': rut.replace("-", "")
        }
        
        if response.status_code == 200:
                respuesta = response.json()
                print(respuesta)
                if isinstance(respuesta, list):
                    return render(request, 'admin/listado-horarios.html', {'context': context})
                elif respuesta.get("message") == "No hay horarios asociados al medico ":
                    print("No hay horas asociadas a este medico")
                    print(respuesta)
                    return render(request, 'admin/listado-horarios.html', {'context': context})
                else:
                    print("No error al obtener horario")
                    messages.warning(request, "No error al obtener horario")
                    print(respuesta)
                    return redirect(to="listado")
        else:
            messages.warning(request, "ERROR API")
            print(respuesta)
            return redirect(to="listado")
    except Exception as ex:
        print("EXCEPCION: ",ex)
        return redirect(to="listado")




def buscarAtencion(request):
    
    
    return render(request , 'admin/buscar-atencion.html')


def eliminarhorario(request, fecha, id, rut, observacion):
    
    rut = agregar_guin_a_rut(rut)
    
    usuario_data = {
        "fecha": fecha,
        "id_horario": id,
        "rut_usuario": rut,
        "observacion": observacion
    }
    data_json = json.dumps(usuario_data)
    
    
    headers = {'Content-Type': 'application/json'}
    
    try:
        url = 'https://apiarquitectura.lusaezd.repl.co/api/horarioMedico/cambiar'
        # Realizar una solicitud POST a la API de Flask para deshabilitar el usuario
        response = requests.post(url, data=data_json, headers=headers)

        # Comprobar si la solicitud fue exitosa (código de estado 201 para creación exitosa)
        if response.status_code == 200:
            respuesta = response.json()
            print("RESPUESTA==============")
            print(respuesta)

            if respuesta.get("correcto") == "Horario anulado correctamente":
                messages.success(request, "Se ha anulado el horario")
            else:
                messages.warning(request, "No se ha anulado el horario")
        else:
            # Manejar errores si la solicitud no fue exitosa
            messages.warning(request,'Error en la respuesta de la API de Flask')

    except requests.exceptions.RequestException:
        messages.warning(request,'Error de conexión a la API de Flask')
    return redirect(to="http://127.0.0.1:8000/listadoHorarioMedico/"+rut)



def lista_usuarios(rut):
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




def agregar_guin_a_rut(rut):
    # Dividir el RUT en parte antes del guion y parte después del guion
    parte1 = rut[:-1]
    parte2 = rut[-1]

    # Concatenar con un guion en el medio
    rut_con_guin = f"{parte1}-{parte2}"

    return rut_con_guin


def cerrar_sesion(request):
    # Realiza la lógica necesaria para cerrar la sesión
    # Por ejemplo, puedes usar request.session.flush() para limpiar toda la sesión
    request.session.flush()
    messages.success(request, "Se ha cerrado la sesion")
    
    # Redirige a la página actual para recargarla
    return redirect(to="inicio")