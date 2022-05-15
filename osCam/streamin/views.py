# import imp
from dataclasses import fields
from pyexpat import model
# import re
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.urls import reverse
# Create your views here.
from django.shortcuts import render
# from .forms import UploadFileForm
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
# from django.views.generic.edit import UpdateView, DeleteView
from osCam.settings import MEDIA_ROOT, MEDIA_URL


from .models import Video

# @ensure_csrf_cookie
# def upload_display_video(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             #print(file.name)
#             handle_uploaded_file(file)
#             return render(request, "upload-display-video.html", {'filename': file.name})
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload-display-video.html', {'form': form})

# def handle_uploaded_file(f):
#     with open(f.name, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

class CreateVideo(CreateView):
    model=Video
    uri_name='create-stream'
    fields=['title', 'description', 'video_file', 'thumbnail']
    template_name = 'streamin/create.html'
    # once form submits sucessfully, send user to DetailView
    # pk is passed into the DetailView URL
    def get_success_url(self) -> str:
        return reverse(DetailView.uri_name, kwargs={'pk': self.object.pk})

class DetailView(DetailView):
    model=Video
    uri_name = 'stream-detail'
    # fields=['title', 'description', 'video_file', 'thumbnail']
    template_name = 'streamin/stream.html'
    # once form submits sucessfully
    # def get_success_url(self) -> str:
    #     return reverse('stream-detail', kwargs={'pk': self.object.pk})
            


def view_gallery_stream(request):
    page = "Video Stream Gallery"
    this_video_list = Video.objects.all()
    stream_data = {'pageTitle':page, 'videos': this_video_list, 'MEDIA_ROOT': MEDIA_ROOT, 'MEDIA_URL': MEDIA_URL}
    # return render_to_response('index.html', )
    
    return render(request, 'streamin/gallery.html', stream_data)
    # return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)

# def add_stream(request):
#     page = "Add Video Stream"
#     return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)
class UpdateVideo(UpdateView):
	model = Video
	fields = ['title', 'description']
	template_name = 'streamin/create.html'

	def get_success_url(self):
		return reverse('video-detail', kwargs={'pk': self.object.pk})

class DeleteVideo(DeleteView):
	model = Video
	template_name = 'streamin/deleteVideo.html'

	def get_success_url(self):
		return reverse('stream')


# def edit_stream(request, id):
#     page = "Edit Video Stream"
#     return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)

# def remove_stream(request, id):
#     page = "View Video Stream"
#     return JsonResponse({'response': request.get_full_path(), 'type':request.method, 'PAGE:': page}, safe=True)