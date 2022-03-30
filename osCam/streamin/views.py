import imp
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
# Create your views here.

def view_stream(request):
    page = "View Video Stream"
    return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)

def add_stream(request):
    page = "Add Video Stream"
    return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)

def edit_stream(request, id):
    page = "Edit Video Stream"
    return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)

def remove_stream(request, id):
    page = "View Video Stream"
    return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)