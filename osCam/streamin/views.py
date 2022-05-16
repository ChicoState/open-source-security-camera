# import imp
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
# from django.views.generic.edit import UpdateView, DeleteView
from osCam.settings import MEDIA_ROOT, MEDIA_URL


from .models import Video


def videoStreamGallery(request):
    pageTitle = "Video Stream Gallery"
    pageData = {
        'response': request.get_full_path(),
        'type': request.method,
        'PAGE_TITLE:': pageTitle,
        'videos': [],
        'MEDIA_URL': '/videos/'
    }
    return JsonResponse(pageData)


@ensure_csrf_cookie
def addStream(request):
    page = "Add Video Stream"
    return JsonResponse(
        {
            'response': request.get_full_path(),
            'type': request.method,
            'PAGE:': page
        },
        safe=True
    )


@ensure_csrf_cookie
def editStream(request, id):
    page = "Edit Video Stream"
    return JsonResponse(
        {
            'response': request.get_full_path(),
            'type': request.method,
            'PAGE:': page
        },
        safe=True
    )


def removeStream(request, id):
    page = "View Video Stream"
    return JsonResponse(
        {
            'response': request.get_full_path(),
            'type': request.method,
            'PAGE:': page
        },
        safe=True
    )
