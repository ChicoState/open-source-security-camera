from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from userconfig.forms import *
from userconfig.models import *

def settings(request):
    this_user = User.objects.get(username=request.user.username)
    from userconfig.models import Camera
    from userconfig.models import CameraView
    from userconfig.models import Storage
    # if there are no cameras create a dummy camera
    if (Camera.objects.count() < 1):
        Camera.objects.create(
            deviceName = 'rpi_camera 01',
        )
    # if there are no views create a dummy view
    if (CameraView.objects.count() < 1):
        CameraView.objects.create(
            showMotionBoxes = 'True',
            showText = 'True',
            text = 'Cam Name :: Date :: Time',
            fps = '30',
            invert = 'False',
            mirror = 'False',
            scale = '0.75'
        )
    # if there are no storages create a dummy storage
    if (Storage.objects.count() < 1):
        Storage.objects.create(
            recordToDevice = 'False',
            filePath = '/home/pi/open-source-security-camera/osCam/videos/',
            maxSpace = '100',
            timeToLive = '60',
            lengthOfRecordings = '10',
        )
    page_data ={
        'cameras': Camera.objects.all(), 
        'views': CameraView.objects.all(), 
        'storages': Storage.objects.all(),
        }
    # save camera settings 
    if(request.method == 'POST'):
        if("add_camera_config" in request.POST):
            add_form = CameraEntryForm(request.POST)
            # check that form is valid
            if(add_form.is_valid()):
                deviceName = add_form.cleaned_data['deviceName']
                this_cam_instance = Camera.objects.get(id=1)
                this_cam_instance.deviceName = deviceName
                this_cam_instance.save()
            return redirect('/settings')
        # save view settings
        elif("add_view_config" in request.POST):
            add_form = CameraViewForm(request.POST)
            if(add_form.is_valid()):
                showMotionBoxes = add_form.cleaned_data['showMotionBoxes']
                showText = add_form.cleaned_data['showText']
                text = add_form.cleaned_data['text']
                fps = add_form.cleaned_data['fps']
                invert = add_form.cleaned_data['invert']
                mirror = add_form.cleaned_data['mirror']
                scale = add_form.cleaned_data['scale']
                # update this instance
                this_view_instance = CameraView.objects.get(id=1)
                this_view_instance.showMotionBoxes = showMotionBoxes
                this_view_instance.showText = showText
                this_view_instance.text = text
                this_view_instance.fps = fps
                this_view_instance.invert = invert
                this_view_instance.mirror = mirror
                this_view_instance.scale = scale
                this_view_instance.save()
            return redirect('/settings')
        # add storage settings
        elif ("add_storage_config" in request.POST):
            add_form = StorageForm(request.POST)
            # check submision form valididity
            if(add_form.is_valid()):
                recordToDevice = add_form.cleaned_data['recordToDevice']
                filePath = add_form.cleaned_data['filePath']
                maxSpace = add_form.cleaned_data['maxSpace']
                timeToLive = add_form.cleaned_data['timeToLive']
                lengthOfRecordings = add_form.cleaned_data['lengthOfRecordings']
                this_storage_instance = Storage.objects.get(id=1)
                this_storage_instance.recordToDevice = recordToDevice
                this_storage_instance.filePath = filePath
                this_storage_instance.maxSpace = maxSpace
                this_storage_instance.timeToLive = timeToLive
                this_storage_instance.lengthOfRecordings = lengthOfRecordings
                this_storage_instance.save()
                return redirect('/settings')
    elif(request.method == "GET"):
        Camera = Camera.objects.get(id=1)
        camera_form_data = CameraEntryForm(
            initial=
            {
                'deviceName': Camera.deviceName,
            }
        )
        Camera = camera_form_data.save(commit = False)
        CameraView = CameraView.objects.get(id=1)
        view_form = CameraViewForm(
            instance=CameraView,
            initial=
            {
                'showMotionBoxes': CameraView.showMotionBoxes,
                'showText': CameraView.showText,
                'text': CameraView.text,
                'fps': CameraView.fps,
                'invert': CameraView.invert,
                'mirror': CameraView.mirror,
                'scale': CameraView.scale,
                }
        )
        CameraView = view_form.save(commit=False)
        Storage = Storage.objects.get(id=1)
        storage_form_data = StorageForm(
            instance=Storage,
            initial={
                'recordToDevice': Storage.recordToDevice,
                'filePath': Storage.filePath,
                'maxSpace': Storage.maxSpace,
                'timeToLive': Storage.timeToLive,
                'lengthOfRecordings': Storage.lengthOfRecordings,
            }
        )
        Storage = storage_form_data.save(commit=False)
        page_data = {
            "camera_form_data": camera_form_data, 
            "view_form_data": view_form, 
            "storage_form_data": storage_form_data,
        }
    return render(request, 'user/settings.html', page_data)
