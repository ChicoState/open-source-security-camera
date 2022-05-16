from time import strftime
from django.shortcuts import redirect, render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from core.models import Recording
from osCam.settings import MEDIA_ROOT, MEDIA_URL



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

def parse_dir_by_date():
    return 'uploads/video_storage/{}'.format(strftime("%Y/%m/%d"))

@ensure_csrf_cookie
def video_stream_edit(request, pk: int):
    page_title = "Edit Video"
    this_video = Recording.objects.get(id=pk)
    edit_video_page_data = {'pageTitle':page_title, 'video': this_video, 'MEDIA_ROOT': MEDIA_ROOT, 'MEDIA_URL': MEDIA_URL}
    return render(request, 'streamin/edit.html', edit_video_page_data)

def view_gallery_stream(request):
    page = "Video Stream Gallery"
    this_video_list = Recording.objects.all()
    stream_data = {'pageTitle':page, 'videos': this_video_list, 'MEDIA_ROOT': MEDIA_ROOT, 'MEDIA_URL': MEDIA_URL}
    
    return render(request, 'streamin/gallery.html', stream_data)

def removeStream(request, pk):
    page = "View Video Stream"
    return JsonResponse(
        {
            'response': request.get_full_path(),
            'type': request.method,
            'PAGE:': page
        },
        safe=True
    )
