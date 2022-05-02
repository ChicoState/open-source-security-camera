from django.test import TestCase
from userconfig.models import User, CameraView, Camera, Storage


class smokeTest(TestCase):
    def test_smoke(self):
        self.assertEqual(1, 1)

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

    def test_user_4(self):
        u = User.objects.create(
          username='@(#)@(#)@EWJEKJWEK',
          password='@(#)@(#)@EWJEKJWEKK')
        self.assertNotEqual(u.username, 'testuser')
        self.assertNotEqual(u.password, 'testpassword')


class CameraViewTestCase(TestCase):
    def testCameraView01(self):
        cv = CameraView.objects.create(
          showMotionBoxes="True",
          showText="True",
          text="test",
          fps="30",
          invert="True",
          mirror="True",
        )
        self.assertEqual(cv.showMotionBoxes, "True")
        self.assertEqual(cv.showText, "True")
        self.assertEqual(cv.text, "test")
        self.assertEqual(cv.fps, "30")
        self.assertEqual(cv.invert, "True")
        self.assertEqual(cv.mirror, "True")

    def testCameraView01(self):
        cv = CameraView.objects.create(
          showMotionBoxes="False",
          showText="False",
          text="test02",
          fps="60",
          invert="False",
          mirror="False",
        )
        self.assertEqual(cv.showMotionBoxes, "False")
        self.assertEqual(cv.showText, "False")
        self.assertEqual(cv.text, "test02")
        self.assertEqual(cv.fps, "60")
        self.assertEqual(cv.invert, "False")
        self.assertEqual(cv.mirror, "False")




class StorageTestCase(TestCase):
    def test_storage_happy_01(self):
        s = Storage.objects.create(
          recordToDevice="True",
          filePath="test",
          maxSpace="1",
          timeToLive="1",
          lengthOfRecordings="1",
        )
        self.assertEqual(s.recordToDevice, "True")
        self.assertEqual(s.filePath, "test")
        self.assertEqual(s.maxSpace, "1")
        self.assertEqual(s.timeToLive, "1")
        self.assertEqual(s.lengthOfRecordings, "1")

    def test_storage_happy_02(self):
      s = Storage.objects.create(
        recordToDevice="False",
        filePath="test01",
        maxSpace="100",
        timeToLive="100",
        lengthOfRecordings="100",
      )
      self.assertEqual(s.recordToDevice, "False")
      self.assertEqual(s.filePath, "test01")
      self.assertEqual(s.maxSpace, "100")
      self.assertEqual(s.timeToLive, "100")
      self.assertEqual(s.lengthOfRecordings, "100")