from ast import Bytes
from ctypes import Union
from dataclasses import dataclass
from typing import Optional
import django
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from numpy import uint32
from .videoportscan import VideoPortScan
from django.urls import reverse
import core.urls
import cv2 as Cv2
from django.contrib.auth.models import User
# Create your tests here.






class SetupMotionDetectCamera(TestCase):
    
    objects = {
        #Constants
        'PORTNUM': 0,
        'URL_NAMEALIAS': 'home',
        'BYTES':b'0',
        'USER_PASSWORD': 'testoscam',
        'USER_FIRST': 'test',
        'USER_LAST': 'testoscam',
        'USER_PHONE':12345678,
        "USER_EMAIL":"test@osCamMail.com",
    }
    @property
    def portNum(self) -> int:
        return self.objects.get("PORTNUM")
    @property
    def urlNameAlias(self) -> str:
        return self.objects.get("URL_NAMEALIAS")
    @property
    def bytes(self) -> bytes:
        return self.objects.get("BYTES")

    def setupVideo(self):
        self.feed = Cv2.VideoCapture(self.portNum)

    def setupUser(self):
        self.user = User.objects.create(
            email=self.objects.get("USER_EMAIL"),
            password=self.objects.get("USER_PASSWORD"),
            first_name=self.objects.get("USER_FIRST"),
            phone=self.objects.get("USER_LAST"),
        )
    # @staticmethod
    def getUrl(self, type, data: Optional[str]= ...):
        if isinstance(type, HttpRequest):
            return HttpRequest.get_full_path()
        elif isinstance(type, HttpResponse):
            # for key in HttpResponse.headers.keys():
                print("[HttpResponse]: ") #,key, HttpResponse.headers[key])   
            # [print("[HttpResponse]: ",key, HttpResponse.headers[key]) ]
        else:
            return reverse(self.urlNameAlias)

    def testEnabled(self):
        self.available, self.working, self.response = VideoPortScan.create().availableAndWorkingPorts()
    

class VideoCapture(SetupMotionDetectCamera):

    def testAddVideoHomePage(self):
        print(f"\n\nCur URL: {self.getUrl(HttpRequest)}")
        _response = self.client.get(self.getUrl(HttpRequest)) #, "Video Test Data Stream"
        # get('/customers/details/', {'name': 'fred', 'age': 7})
        self.assertEqual(_response.status_code, 200)
        self.assertTemplateUsed(response=_response, template_name="core/home.html")
    def invalidVideoDataView(self):
        self.assertEquals(reverse("home"), HttpRequest.get_host())
        _response = self.client.post()
