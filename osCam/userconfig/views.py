from ipaddress import ipAddress
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

    from userconfig.models import cameraView

     # if there are no cameras create a dummy camera
    if (Camera.objects.count() <= 1):
        Camera.objects.create(
            modelNum = '04',
            modelName = 'Raspberry Pi Camera',
            cameraIndex = '0',
            deviceName = 'rpi_camera 01',
            ipAddress = '10.0.0.94',
            port = '8000',
        )

    # if there are no views create a dummy view
    if (cameraView.objects.count() <= 1):
        cameraView.objects.create(
            showMotionBoxes = 'True',
            showContours = 'False',
            showText = 'True',
            text = 'Cam Name :: Date :: Time',
            contrast = '50',
            brightness = '50',
            recording = 'True',
            fps = '30',
            invert = 'False',
            mirror = 'False',
        )

    this_user = User.objects.get(username=request.user)
    
    page_data = {'cameras': Camera.objects.all(), 'views': cameraView.objects.all(),}

    if(request.method == 'POST'):
        if("add_camera_config" in request.POST):
            add_form = CameraEntryForm(request.POST)
            if(add_form.is_valid()):
                deviceName = add_form.cleaned_data['deviceName']
                ipAddress = add_form.cleaned_data['ipAddress']
                port = add_form.cleaned_data['port']

                Camera(
                    user=this_user,
                    deviceName=deviceName,
                    ipAddress=ipAddress,
                    port=port,
                ).save()

            return redirect('/config/')

        elif("add_view_config" in request.POST):
            add_form = ViewForm(request.POST)
            if(add_form.is_valid()):
                showMotionBoxes = add_form.cleaned_data['showMotionBoxes']
                showContours = add_form.cleaned_data['showContours']
                showText = add_form.cleaned_data['showText']
                text = add_form.cleaned_data['text']
                contrast = add_form.cleaned_data['contrast']
                brightness = add_form.cleaned_data['brightness']
                recording = add_form.cleaned_data['recording']
                fps = add_form.cleaned_data['fps']
                invert = add_form.cleaned_data['invert']
                mirror = add_form.cleaned_data['mirror']

                cameraView(
                    showMotionBoxes=showMotionBoxes,
                    showContours=showContours,
                    showText=showText,
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
        cameraView = cameraView.objects.get(id=1)
        view_form = ViewForm(instance=cameraView,
        initial={
            'showMotionBoxes': cameraView.showMotionBoxes,
            'showContours': cameraView.showContours,
            'showText': cameraView.showText,
            'text': cameraView.text,
            'contrast': cameraView.contrast,
            'brightness': cameraView.brightness,
            'recording': cameraView.recording,
            'fps': cameraView.fps,
            'invert': cameraView.invert,
            'mirror': cameraView.mirror,
        })
        cameraView = view_form.save(commit=False)

        page_data = {
            "camera_form_data": CameraEntryForm(), "view_form_data": view_form, 
        }

    return render(request, 'user/add_config.html', page_data)