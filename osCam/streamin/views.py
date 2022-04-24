# import imp
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

def view_stream_gallery(request):
    pageTitle = "Video Stream Gallery"
    pageData = {
        'response': request.get_full_path(), 
        'type':request.method, 
        'PAGE_TITLE:': pageTitle, 
        'videos':[], 
        'MEDIA_URL': '/videos/'
    }
    return JsonResponse(pageData)

@ensure_csrf_cookie
def add_stream(request):
    page = "Add Video Stream"
    return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)

@ensure_csrf_cookie
def edit_stream(request, id):
    page = "Edit Video Stream"
    return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)

def remove_stream(request, id):
    page = "View Video Stream"
    return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)