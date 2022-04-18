# import imp
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
# Create your views here.
from django.shortcuts import render
from .forms import UploadFileForm
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def upload_display_video(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            #print(file.name)
            handle_uploaded_file(file)
            return render(request, "upload-display-video.html", {'filename': file.name})
    else:
        form = UploadFileForm()
    return render(request, 'upload-display-video.html', {'form': form})

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

            
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