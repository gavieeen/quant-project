# from django.shortcuts import render
# from django.http import HttpResponse

# # Create your views here.

# def index(request):
#     return HttpResponse("Quant Project")

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
