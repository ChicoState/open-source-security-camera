from ipaddress import ip_address
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json as Json

# from core import models
from userconfig.models import Network, Camera, RaspberryPi
from django.contrib.auth.models import User
from .forms import CameraEntryForm
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
    if page_data['cameras'].exists():
        page_data['cameras'][0] = 'camera 1'


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

def addConf(request):
    '''
        View Handles Http response To [ADD] a new Configuration.
            Configuration Could be of Type {RaspberryPi, Camera, Network}
        
        @param  request: Request 
    '''
    page = "Add Config"

    network_info={"SERVER_NAME": None, "GATEWAY_INTERFACE":None,"SERVER_PORT":None,
    "REMOTE_HOST":None,"CONTENT_LENGTH":None,"SERVER_PROTOCOL":None,
    "SERVER_SOFTWARE":None,"REQUEST_METHOD":None,"PATH_INFO":None,
    "QUERY_STRING":None,"REMOTE_ADDR":None,"CONTENT_TYPE":None,"HTTP_HOST":None}
     # get the info from httpRequest parameter so we can later use user_id as 'accessor' for our database records
    this_user = User.objects.get(id=request.user.id)
    if network_info['REMOTE_ADDR'] is None:     # should query the Network Model to check if Network is Already saved for the user so we can auto-populate in corresponding Form
        meta = request.META
        for key in meta.keys():
            if key == 'SERVER_NAME' or key == 'SERVER_PORT' \
            or key=='REMOTE_ADDR' or key=='REMOTE_ADDR' \
            or key=='HTTP_HOST':
                network_info[key] = meta[key]
                Network(user=this_user,home_ip_address=network_info['REMOTE_ADDR'], camera_ip_address=network_info['REMOTE_ADDR']).save() 
            # print(key, meta[key] )    # print this to see all Network Information supplied by Django and network packet. If we want more we need send out ARP or get from user directly. 
    # Network(request.get_host())
    #return JsonResponse({'response': 'SUCCESS', 'type':'GET', 'Client IP Address': network_info['REMOTE_ADDR'], 'PAGE': page}, safe=True)
    page_data = {'cameras': Camera.objects.all(), 'raspberrypis': RaspberryPi.objects.all(), 'networks': Network.objects.all()}

    

    if(request.method == 'POST'):
        if("add" in request.POST):
            add_form = CameraEntryForm(request.POST)
            if(add_form.is_valid()):
                recording = add_form.cleaned_data['recording']

            # create camera object w the form data
            # save camera object
            Camera(user=this_user, recording=recording).save()

            return redirect('/')
    else:
        page_data = {
            "form_data": CameraEntryForm()
        }
    return render(request, 'user/add_config.html', page_data)


def editConf(request, id):
    '''
        View Handles response To [EDIT] a Configuration of Type::{RaspberryPi, Camera, Network}
        
        @param  request: Request 
                id: Integer
    '''
    page = "Edit Config"
    return JsonResponse({'response': 'SUCCESS', 'type':'GET', 'PAGE': page}, safe=True)




def removeConf(request, id):
    '''
        View Handles response To [REMOVE] a Configuration of Type::{RaspberryPi, Camera, Network}
        @param  request: Request 
                id: Integer
    '''
    page = "Remove Config"
    return JsonResponse({'response': 'SUCCESS', 'type':'GET', 'PAGE:': page}, safe=True)