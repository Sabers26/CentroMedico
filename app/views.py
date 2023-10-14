from django.shortcuts import render

# Create your views here.

def inicio(request):
    return render(request, 'index.html')

def addColaboradores(request):
    return render(request, 'colaboradores.html')