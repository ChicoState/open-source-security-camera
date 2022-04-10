from ipaddress import ip_address
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json as Json

from numpy import record

from userconfig.models import *
from userconfig.models import Network, Camera, RaspberryPi
from userconfig.forms import *

def settings(request):
    '''
        View Handles Http response To [ADD] a new Configuration.
            Configuration Could be of Type {RaspberryPi, Camera, Network}
        
        @param  request: Request 
    '''

    from userconfig.models import camera_view

     # if there are no cameras create a dummy camera
    if (Camera.objects.count() <= 1):
        Camera.objects.create(
            model_num = '04',
            model_name = 'Raspberry Pi Camera',
            camera_index = '0',
            device_name = 'rpi_camera 01',
            ip_address = '10.0.0.94',
            port = '8000',
        )

    # if there are no views create a dummy view
    if (camera_view.objects.count() <= 1):
        camera_view.objects.create(
            show_motion_boxes = 'True',
            show_contours = 'False',
            show_text = 'True',
            text = 'Cam Name :: Date :: Time',
            contrast = '50',
            brightness = '50',
            recording = 'True',
            fps = '30',
            invert = 'False',
            mirror = 'False',
        )

    this_user = User.objects.get(username=request.user)
    
    page_data = {'cameras': Camera.objects.all(), 'views': camera_view.objects.all(),}

    if(request.method == 'POST'):
        if("add_camera_config" in request.POST):
            add_form = CameraEntryForm(request.POST)
            if(add_form.is_valid()):
                device_name = add_form.cleaned_data['device_name']
                ip_address = add_form.cleaned_data['ip_address']
                port = add_form.cleaned_data['port']

                Camera(
                    user=this_user,
                    device_name=device_name,
                    ip_address=ip_address,
                    port=port,
                ).save()

            return redirect('/config/')

        elif("add_view_config" in request.POST):
            add_form = ViewForm(request.POST)
            if(add_form.is_valid()):
                show_motion_boxes = add_form.cleaned_data['show_motion_boxes']
                show_contours = add_form.cleaned_data['show_contours']
                show_text = add_form.cleaned_data['show_text']
                text = add_form.cleaned_data['text']
                contrast = add_form.cleaned_data['contrast']
                brightness = add_form.cleaned_data['brightness']
                recording = add_form.cleaned_data['recording']
                fps = add_form.cleaned_data['fps']
                invert = add_form.cleaned_data['invert']
                mirror = add_form.cleaned_data['mirror']

                camera_view(
                    show_motion_boxes=show_motion_boxes,
                    show_contours=show_contours,
                    show_text=show_text,
                    text=text,
                    contrast=contrast,
                    brightness=brightness,
                    recording=recording,
                    fps=fps,
                    invert=invert,
                    mirror=mirror,
                ).save()
                return redirect('/config/')

    elif(request.method == "GET"):
        camera_view = camera_view.objects.get(id=1)
        view_form = ViewForm(instance=camera_view,
        initial={
            'show_motion_boxes': camera_view.show_motion_boxes,
            'show_contours': camera_view.show_contours,
            'show_text': camera_view.show_text,
            'text': camera_view.text,
            'contrast': camera_view.contrast,
            'brightness': camera_view.brightness,
            'recording': camera_view.recording,
            'fps': camera_view.fps,
            'invert': camera_view.invert,
            'mirror': camera_view.mirror,
        })
        camera_view = view_form.save(commit=False)

        page_data = {
            "camera_form_data": CameraEntryForm(), "view_form_data": view_form, 
        }

    return render(request, 'user/add_config.html', page_data)