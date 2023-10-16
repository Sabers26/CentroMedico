from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request, 'index.html')

def addColaboradores(request):
    return render(request, 'colaboradores.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')