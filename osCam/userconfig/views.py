from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from userconfig.forms import *
from userconfig.models import *

def settings(request):

    from userconfig.models import Camera

    this_user = User.objects.get(username=request.user.username)

    # if there is no Network settings, create
    if (Network.objects.count() < 1):
        Network.objects.create(
            user=this_user,
            homeIpAddress = '192.168.0.69',
            homeNetmask = '255.255.0.0',
            cameraIpAddress = '192.168.0.70',
        )

    # if there are no pis, create a starter pi 
    if (RaspberryPi.objects.count() < 1):
        RaspberryPi.objects.create(
            user = this_user,
            modelName = 'model name',
            modelNum = '1234',
            username = 'username',
            password = 'password',
            network = Network.objects.get(id=1),
        )

    # if there are no cameras create a dummy camera
    if (Camera.objects.count() < 1):
        Camera.objects.create(
            modelNum = '04',
            raspberryPi = RaspberryPi.objects.get(id=1),
            modelName = 'model name',
            cameraIndex = '0',
            deviceName = 'rpi_camera 01',
            ipAddress = '10.0.0.94',
            port = '8000',
        )

    from userconfig.models import CameraView
    # if there are no views create a dummy view
    if (CameraView.objects.count() < 1):
        CameraView.objects.create(
            # camera = Camera.objects.get(id='1'),
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

    from userconfig.models import Storage
    # if there are no storages create a dummy storage
    if (Storage.objects.count() < 1):
        Storage.objects.create(
            recordToDevice = 'False',
            recordToCloud = 'False',
            filePath = '/home/pi/open-source-security-camera/osCam/videos/',
            maxSpace = '100',
            timeToLive = '60',
            archive = 'False',
            lengthOfRecordings = '10',
            codec = 'h264',
        )
    
    page_data = {
        'cameras': Camera.objects.all(), 
        'views': CameraView.objects.all(), 
        'network': Network.objects.get(id=1),
        'storages': Storage.objects.all(),
        'raspberrypis': RaspberryPi.objects.all(),
        }

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
            add_form = CameraViewForm(request.POST)
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

                this_view_instance = CameraView.objects.get(id=1)
                this_view_instance.showMotionBoxes = showMotionBoxes
                this_view_instance.showContours = showContours
                this_view_instance.showText = showText
                this_view_instance.text = text
                this_view_instance.contrast = contrast
                this_view_instance.brightness = brightness
                this_view_instance.recording = recording
                this_view_instance.fps = fps
                this_view_instance.invert = invert
                this_view_instance.mirror = mirror
                this_view_instance.save()

            return redirect('/config/')

        elif ("add_storage_config" in request.POST):
            add_form = StorageForm(request.POST)
            if(add_form.is_valid()):
                recordToDevice = add_form.cleaned_data['recordToDevice']
                recordToCloud = add_form.cleaned_data['recordToCloud']
                filePath = add_form.cleaned_data['filePath']
                maxSpace = add_form.cleaned_data['maxSpace']
                timeToLive = add_form.cleaned_data['timeToLive']
                archive = add_form.cleaned_data['archive']
                lengthOfRecordings = add_form.cleaned_data['lengthOfRecordings']
                codec = add_form.cleaned_data['codec']

                this_storage_instance = Storage.objects.get(id=1)
                this_storage_instance.recordToDevice = recordToDevice
                this_storage_instance.recordToCloud = recordToCloud
                this_storage_instance.filePath = filePath
                this_storage_instance.maxSpace = maxSpace
                this_storage_instance.timeToLive = timeToLive
                this_storage_instance.archive = archive
                this_storage_instance.lengthOfRecordings = lengthOfRecordings
                this_storage_instance.codec = codec
                this_storage_instance.save()

                return redirect('/config/')
                
        elif ("add_network_config" in request.POST):
            add_form = NetworkEntryForm(request.POST)
            if(add_form.is_valid()):
                homeIpAddress = add_form.cleaned_data['homeIpAddress']
                homeNetmask = add_form.cleaned_data['homeNetmask']
                cameraIpAddress = add_form.cleaned_data['cameraIpAddress']

                this_network_instance = Network.objects.get(id=1)
                this_network_instance.homeIpAddress = homeIpAddress
                this_network_instance.homeNetmask = homeNetmask
                this_network_instance.cameraIpAddress = cameraIpAddress
                this_network_instance.save()

                return redirect('/config/')

    elif(request.method == "GET"):
        CameraView = CameraView.objects.get(id=1)
        view_form = CameraViewForm(instance=CameraView,
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
            "camera_form_data": CameraEntryForm(), 
            "view_form_data": view_form, 
            "storage_form_data": StorageForm(),
            "network_form_data": NetworkEntryForm(),
        }

    return render(request, 'user/add_config.html', page_data)