from ipaddress import ip_address
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json as Json

from numpy import record
from userconfig.models import *

# from core import models
from userconfig.models import Network, Camera, RaspberryPi
from django.contrib.auth.models import User
from userconfig.forms import *
# from userconfig.models import Network

################################
################################
#  Views used for User Configurations: .
#       e.g. A Config is of Type::{RaspberryPi, Camera, Network}
def configPage(request):
    '''
        View Handles Http response To Display all user defined Configuration.
            Configuration Could be of Type::{RaspberryPi, Camera, Network}.
        
        @param  request: Request 
    '''
    page = "User Configuration Page"
    page_data = {'cameras': Camera.objects.all(), 'raspberrypis': RaspberryPi.objects.all(), 'networks': Network.objects.all()}
    
    response = {'response':None}
    if request.method == 'GET':
        print('HOST: ', request.get_host())
        user = User.objects.get(id=request.user.id)
        print("User Id:: ", user.id)
        # buildable_str = f"{user.id} + "
        lookup =  Network.objects.filter(user=user)
        usermp = []
        for record in Network.objects.all():
            if record is not None:
                if record.user is not None:
                    name = record.user.username
                    name_id = record.user.id
                    ip_addr = record.home_ip_address
                    print(name)
                    print(name_id)
                    print(ip_addr)
                    usermp.append({"username": name, "user_id":name_id, "IP ADDRESS":ip_addr})

        content = Json.dumps(usermp)
    #return JsonResponse({'response': 'SUCCESS', 'type':'GET', "Client-IP::LOOKUP":content, 'PAGE': page, 'data':response.get('response')}, safe=True)

    # if there are no cameras create a dummy camera
    # if page_data['cameras'].exists():
    #    page_data['cameras'][0] = 'camera 1'


    return render(request, 'user/config.html', page_data)


# SERVER_NAME localhost
# GATEWAY_INTERFACE CGI/1.1
# SERVER_PORT 8000
# REMOTE_HOST
# CONTENT_LENGTH
# SCRIPT_NAME
# SERVER_PROTOCOL HTTP/1.1
# SERVER_SOFTWARE WSGIServer/0.2
# REQUEST_METHOD GET
# PATH_INFO /config/
# QUERY_STRING
# REMOTE_ADDR 127.0.0.1
# CONTENT_TYPE text/plain
# HTTP_HOST 127.0.0.1:8000

def settings(request):
    '''
        View Handles Http response To [ADD] a new Configuration.
            Configuration Could be of Type {RaspberryPi, Camera, Network}
        
        @param  request: Request 
    '''

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
            text = 'Text overlayed on the feed',
            contrast = '50',
            brightness = '50',
            recording = 'True',
            fps = '30',
            invert = 'False',
            mirror = 'False',
        )

    # get the info from httpRequest parameter so we can later use user_id as 'accessor' for our database records
    this_user = User.objects.get(id=request.user.id)
    
    page_data = {'cameras': Camera.objects.all(), 'views': camera_view.objects.all(),}

    if(request.method == 'POST'):
        if("add_camera_config" in request.POST):
            add_form = CameraEntryForm(request.POST)
            if(add_form.is_valid()):
                device_name = add_form.cleaned_data['device_name']
                ip_address = add_form.cleaned_data['ip_address']
                port = add_form.cleaned_data['port']
                #recording = add_form.cleaned_data['recording']
                #fps = add_form.cleaned_data['fps']
                #invert = add_form.cleaned_data['invert']
                #mirror = add_form.cleaned_data['mirror']
                #codec = add_form.cleaned_data['codec']  

                # create camera object w the form data
                # save camera object
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

                camera_view.objects.create(
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
                )
    else:
        page_data = {
            "camera_form_data": CameraEntryForm(), "view_form_data": ViewForm() 
        }
    return render(request, 'user/add_config.html', page_data)