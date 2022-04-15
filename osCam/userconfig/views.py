from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from userconfig.forms import *
from userconfig.models import *

def settings(request):

    from userconfig.models import Camera

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

    from userconfig.models import CameraView

    # if there are no views create a dummy view
    if (CameraView.objects.count() <= 1):
        CameraView.objects.create(
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
    
    page_data = {'cameras': Camera.objects.all(), 'views': CameraView.objects.all(),}

    # save camera settings 
    if(request.method == 'POST'):
        if("add_camera_config" in request.POST):
            add_form = CameraEntryForm(request.POST)
            if(add_form.is_valid()):
                deviceName = add_form.cleaned_data['deviceName']
                ipAddress = add_form.cleaned_data['ipAddress']
                port = add_form.cleaned_data['port']

                this_cam_instance = Camera.objects.get(id=1)
                this_cam_instance.deviceName = deviceName
                this_cam_instance.ipAddress = ipAddress
                this_cam_instance.port = port
                this_cam_instance.save()

            return redirect('/config/')

        # save view settings
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

                CameraView(
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
        CameraView = CameraView.objects.get(id=1)
        view_form = ViewForm(instance=CameraView,
        initial={
            'showMotionBoxes': CameraView.showMotionBoxes,
            'showContours': CameraView.showContours,
            'showText': CameraView.showText,
            'text': CameraView.text,
            'contrast': CameraView.contrast,
            'brightness': CameraView.brightness,
            'recording': CameraView.recording,
            'fps': CameraView.fps,
            'invert': CameraView.invert,
            'mirror': CameraView.mirror,
        })
        CameraView = view_form.save(commit=False)

        page_data = {
            "camera_form_data": CameraEntryForm(), "view_form_data": view_form, 
        }

    return render(request, 'user/add_config.html', page_data)