from django.shortcuts import render

def hello_word(request):
    return render(request, 'usuarios.html')