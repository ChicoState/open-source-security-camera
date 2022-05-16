import django
from dataclasses import dataclass
from typing import Optional
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from .videoportscan import VideoPortScan
from django.urls import reverse
import core.urls
import cv2 as Cv2
from django.contrib.auth.models import User
# Create your tests here.

class smokeTest(TestCase):
    def test_smoke(self):
        self.assertEqual(1, 1)

class SetupMotionDetectCamera(TestCase):
    
    objects = {
        #Constants
        'PORTNUM': 0,
        'URL_NAMEALIAS': 'home',
        'BYTES':b'0',
        'USER_PASSWORD': 'testoscam',
        'USER_NAME': 'tester',
        'USER_FIRST': 'test',
        'USER_LAST': 'testoscam',
        'USER_PHONE':12345678,
        "USER_EMAIL":"test@osCamMail.com",
        'USER_NAME2': 'admin',
        'USER_FIRST2':'admin',
        'USER_LAST2': 'admin',
        'USER2_PASS':'testoadmin',
    }
    @property
    def portNum(self) -> int:
        return self.objects.get("PORTNUM")
    @property
    def urlNameAlias(self) -> str:
        return self.objects.get("URL_NAMEALIAS")

    def setupUser(self):
        self.user = User.objects.create(
            email=self.objects.get("USER_EMAIL"),
            password=self.objects.get("USER_PASSWORD"),
            username=self.objects.get("USER_NAME2"),
        )
        return self.user
    
    def getUser(self) -> User:
        if self.user is None:
            return None 
        else:
            return User.objects.get(id=self.user.id)


    def setupSecondUser(self):
        self.user2 = User.objects.create(
            email=self.objects.get("USER_EMAIL"),
            password=self.objects.get("USER_PASSWORD"),
            username=self.objects.get("USER2_NAME"),
        )

    def getSecondUser(self) -> User:
        if self.user2 is None:
            return None 
        else:
            return User.objects.get(id=self.user2.id)
        
    def getUrl(self, type, data: Optional[str]= ...):
        if isinstance(type, HttpRequest):
            return HttpRequest.get_full_path()
        else:
            return reverse(self.urlNameAlias)

    def testEnabled(self):
        self.available, self.working, self.response = VideoPortScan.create().availableAndWorkingPorts()
    
class VideoCapture(SetupMotionDetectCamera):

    def testAddHomePageRickRolled(self):
        respon = self.client.get('/') #, "Video Test Data Stream"
        print(f"\n\nCur URL: {self.getUrl('home')} \n url:  SATUS={respon.status_code}")
        self.client.login(
            username=self.objects.get('USER_NAME2'), 
            password= self.objects.get('USER2_PASS')
            )
        self.assertEqual(respon.status_code, 302)

    def testHomePageTemplate(self):
        _response = self.client.get('') 
        self.client.login(
            username=self.objects.get('USER_NAME2'), 
            password= self.objects.get('USER2_PASS')
            )
        _logged_in_resp = self.client.post('/login/', {'username': self.objects.get('USER_NAME2'), 'password': self.objects.get('USER2_PASS')})
        self.assertTrue(_logged_in_resp.status_code==200)
    
    def invalidVideoDataView(self):
        self.assertEquals(reverse("home"), HttpRequest.get_host())
        _response = self.client.post()

