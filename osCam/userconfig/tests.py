from django.test import TestCase
from userconfig.models import *

class smokeTest(TestCase):
    def test_smoke(self):
        self.assertEqual(1, 1)
    def test_joke(self):
        x = 69
        self.assertNotEqual(x, 420)

class userTest(TestCase):
    def test_user(self):
        u = User.objects.create(
          username='testuser', 
          password='testpassword')
        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.password, 'testpassword')
    def test_user_2(self):
        u = User.objects.create(
          username='KAJLHSF*(#UIONFN', 
          password='KMFK(I*(*$(#KF')
        self.assertEqual(u.username, 'KAJLHSF*(#UIONFN')
        self.assertEqual(u.password, 'KMFK(I*(*$(#KF')
    def test_user_3(self):
        u = User.objects.create(
          username='testuser', 
          password='testpassword')
        self.assertNotEqual(u.username, 'KAJLHSF*(#UIONFN')
        self.assertNotEqual(u.password, 'KMFK(I*(*$(#KF')

class NetworkTestCase(TestCase):
    def test_network(self):
        n = Network.objects.create(
          homeIpAddress = "10.0.0.94",
          homeNetmask = "255.255.255.0",
          cameraIpAddress = "10.0.0.94",
          user = User.objects.create(
            username='testuser',
            password='testpassword'))
        self.assertEqual(n.homeIpAddress, "10.0.0.94")
        self.assertEqual(n.homeNetmask, "255.255.255.0")
        self.assertEqual(n.cameraIpAddress, "10.0.0.94")
        self.assertEqual(n.user.username, "testuser")
        self.assertEqual(n.user.password, "testpassword")

class RaspberryPiTestCase(TestCase):
    def test_raspberrypi(self):
        u = User.objects.create(
          username='testuser',
          password='testpassword')
        r = RaspberryPi.objects.create(
          user = u,
          network = Network.objects.create(
            homeIpAddress = "10.0.0.94",
            homeNetmask = "255.255.255.0",
            cameraIpAddress = "10.0.0.94",
            user = u),
          modelNum = "4",
          modelName = "Raspberry Pi B+",
          username = "pi",
          password = "raspberry"
      )
        self.assertEqual(r.user.username, "testuser")
        self.assertEqual(r.user.password, "testpassword")
        self.assertEqual(r.network.homeIpAddress, "10.0.0.94")
        self.assertEqual(r.network.homeNetmask, "255.255.255.0")
        self.assertEqual(r.network.cameraIpAddress, "10.0.0.94")
        self.assertEqual(r.modelNum, "4")
        self.assertEqual(r.modelName, "Raspberry Pi B+")
        self.assertEqual(r.username, "pi")
        self.assertEqual(r.password, "raspberry")

    def test_raspberrypi_2(self):
        u = User.objects.create(
          username='testuserTESTINGTESTING',
          password='testpasswordTESTINGTESTING')
        r = RaspberryPi.objects.create(
          user = u,
          network = Network.objects.create(
            homeIpAddress = "127.192.168.0",
            homeNetmask = "255.255.255.0",
            cameraIpAddress = "127.192.168.1",
            user = u),
          modelNum = "3",
          modelName = "Raspberry Pi C",
          username = "pipipipipipi",
          password = "passpasspass"
      )
        self.assertEqual(r.user.username, "testuserTESTINGTESTING")
        self.assertEqual(r.user.password, "testpasswordTESTINGTESTING")
        self.assertEqual(r.network.homeIpAddress, "127.192.168.0")
        self.assertEqual(r.network.homeNetmask, "255.255.255.0")
        self.assertEqual(r.network.cameraIpAddress, "127.192.168.1")
        self.assertEqual(r.modelNum, "3")
        self.assertEqual(r.modelName, "Raspberry Pi C")
        self.assertEqual(r.username, "pipipipipipi")
        self.assertEqual(r.password, "passpasspass")

class CameraTestCase(TestCase):
    def test_camera(self):
        u = User.objects.create(
          username='testuser',
          password='testpassword')
        r = RaspberryPi.objects.create(
          user = u,
          network = Network.objects.create(
            homeIpAddress = "127.192.168.0",
            homeNetmask = "255.255.255.0",
            cameraIpAddress = "127.192.168.1",
            user = u),
          modelNum = "3",
          modelName = "Raspberry Pi C",
          username = "pipipipipipi",
          password = "passpasspass"
      )
        c = Camera.objects.create(
          user = u,
          raspberryPi = r,
          modelNum = "1",
          modelName = "Mode 1",
          cameraIndex = "0",
          deviceName = "Camera 1",
          ipAddress = "127.0.0.1",
          port = "8080",)
        self.assertEqual(c.user.username, "testuser")
        self.assertEqual(c.user.password, "testpassword")
        self.assertEqual(c.raspberryPi.user.username, "testuser")
        self.assertEqual(c.raspberryPi.user.password, "testpassword")
        self.assertEqual(c.raspberryPi.network.homeIpAddress, "127.192.168.0")
        self.assertEqual(c.raspberryPi.network.homeNetmask, "255.255.255.0")
        self.assertEqual(c.raspberryPi.network.cameraIpAddress, "127.192.168.1")
        self.assertEqual(c.raspberryPi.modelNum, "3")
        self.assertEqual(c.raspberryPi.modelName, "Raspberry Pi C")
        self.assertEqual(c.raspberryPi.username, "pipipipipipi")
        self.assertEqual(c.raspberryPi.password, "passpasspass")
        self.assertEqual(c.modelNum, "1")
        self.assertEqual(c.modelName, "Mode 1")
        self.assertEqual(c.cameraIndex, "0")
        self.assertEqual(c.deviceName, "Camera 1")
        self.assertEqual(c.ipAddress, "127.0.0.1")
        self.assertEqual(c.port, "8080")

class CameraViewTestCase(TestCase):
    def test_camera_view(self):
        u = User.objects.create(
          username='testuser',
          password='testpassword')
        cv = CameraView.objects.create(
          showMotionBoxes = "True",
          showContours = "True",
          showText = "True",
          text = "test",
          contrast = "1",
          brightness = "1",
          recording = "True",
          fps = "1",
          invert = "True",
          mirror = "True",
        )
        self.assertEqual(cv.showMotionBoxes, "True")
        self.assertEqual(cv.showContours, "True")
        self.assertEqual(cv.showText, "True")
        self.assertEqual(cv.text, "test")
        self.assertEqual(cv.contrast, "1")
        self.assertEqual(cv.brightness, "1")
        self.assertEqual(cv.recording, "True")
        self.assertEqual(cv.fps, "1")
        self.assertEqual(cv.invert, "True")
        self.assertEqual(cv.mirror, "True")

class StorageTestCase(TestCase):
    def test_storage(self):
        u = User.objects.create(
          username='testuser',
          password='testpassword')
        s = Storage.objects.create(
          recordToDevice = "True",
          recordToCloud = "True",
          filePath = "test",
          maxSpace = "1",
          timeToLive = "1",
          archive = "True",
          lengthOfRecordings = "1",
          codec = "1",
        )
        self.assertEqual(s.recordToDevice, "True")
        self.assertEqual(s.recordToCloud, "True")
        self.assertEqual(s.filePath, "test")
        self.assertEqual(s.maxSpace, "1")
        self.assertEqual(s.timeToLive, "1")
        self.assertEqual(s.archive, "True")
        self.assertEqual(s.lengthOfRecordings, "1")
        self.assertEqual(s.codec, "1")
