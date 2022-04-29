# import imp
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie


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
