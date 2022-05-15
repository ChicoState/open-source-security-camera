from django.test import TestCase
from userconfig.models import CustomUser, CameraView, Camera, Storage
from userconfig.forms import CameraEntryForm, CameraViewForm, StorageForm

class smokeTest(TestCase):
    def test_smoke(self):
        self.assertEqual(1, 1)

    def test_joke(self):
        x = 69
        self.assertNotEqual(x, 420)

class userTest(TestCase):
    def test_user(self):
        u = CustomUser.objects.create(
          username='testuser',
          password='testpassword')
        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.password, 'testpassword')

    def test_user_2(self):
        u = CustomUser.objects.create(
          username='KAJLHSF*(#UIONFN',
          password='KMFK(I*(*$(#KF')
        self.assertEqual(u.username, 'KAJLHSF*(#UIONFN')
        self.assertEqual(u.password, 'KMFK(I*(*$(#KF')

    def test_user_3(self):
        u = CustomUser.objects.create(
          username='testuser',
          password='testpassword')
        self.assertNotEqual(u.username, 'KAJLHSF*(#UIONFN')
        self.assertNotEqual(u.password, 'KMFK(I*(*$(#KF')
    
    def test_user_4(self):
        u = CustomUser.objects.create(
          username='testuser',
          password='testpassword')
        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.password, 'testpassword')


class CameraTestCase(TestCase):
    def test_camera(self):
        c = Camera.objects.create(
          deviceName="Camera 1",
        )
        u = CustomUser.objects.create(
          username='testuser',
          password='testpassword')
        c.user = u
        self.assertEqual(c.user.username, "testuser")
        self.assertEqual(c.user.password, "testpassword")
        self.assertEqual(c.deviceName, "Camera 1")


class CameraViewTestCase(TestCase):
    def test_camera_view(self):
        cv = CameraView.objects.create(
          showMotionBoxes="True",
          showText="True",
          text="test",
          fps="1",
          invert="True",
          mirror="True",
        )
        self.assertEqual(cv.showMotionBoxes, "True")
        self.assertEqual(cv.showText, "True")
        self.assertEqual(cv.text, "test")
        self.assertEqual(cv.fps, "1")
        self.assertEqual(cv.invert, "True")
        self.assertEqual(cv.mirror, "True")


class StorageTestCase(TestCase):
    def test_storage(self):
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

class StorageFormTestCase(TestCase):
    def test_storage_form_valid(self):
        form = StorageForm(data={
          'recordToDevice': 'True',
          'filePath': 'test',
          'maxSpace': '1',
          'timeToLive': '1',
          'lengthOfRecordings': '1',
        })
        self.assertTrue(form.is_valid())

    def test_storage_form_2_valid(self):
        form = StorageForm(data={
          'recordToDevice': 'False',
          'filePath': 'test2',
          'maxSpace': '100',
          'timeToLive': '100',
          'lengthOfRecordings': '100',
        })
        self.assertTrue(form.is_valid())

    def test_storage_form_3_valid(self):
      form = StorageForm(data={
        'recordToDevice': 'True',
        'filePath': 'test3',
        'maxSpace': '100',
        'timeToLive': '100',
        'lengthOfRecordings': '100',
      })
      self.assertEqual(form.is_valid(), True)

    def test_storage_form_labels(self):
      form = StorageForm(data={
        'recordToDevice': 'True',
        'filePath': 'test4',
        'maxSpace': '100',
        'timeToLive': '100',
        'lengthOfRecordings': '100',
      })
      self.assertEqual(form.is_valid(), True)
      self.assertEqual(form.fields['recordToDevice'].label, 'Record to Device')
      self.assertEqual(form.fields['filePath'].label, "File Path")
      self.assertEqual(form.fields['maxSpace'].label, "Max Space")
      self.assertEqual(form.fields['timeToLive'].label, "Time to Live")
      self.assertEqual(form.fields['lengthOfRecordings'].label, "Length of Recordings")
    
    def test_storage_form_initials_01(self):
      form = StorageForm(data={
        'recordToDevice': 'True',
        'filePath': 'testLabel',
        'maxSpace': '100',
        'timeToLive': '100',
        'lengthOfRecordings': '100',
      })
      self.assertEqual(form.is_valid(), True)
      self.assertEqual(form.fields['recordToDevice'].initial, None)
      self.assertEqual(form.fields['filePath'].initial, None)
      self.assertEqual(form.fields['maxSpace'].initial, None)
      self.assertEqual(form.fields['timeToLive'].initial, None)
      self.assertEqual(form.fields['lengthOfRecordings'].initial, None)

    def test_storage_form_initials_02(self):
      form = StorageForm(data={
        'recordToDevice': 'False',
        'filePath': 'testLabel05',
        'maxSpace': '10000',
        'timeToLive': '10000',
        'lengthOfRecordings': '10000',
      })
      self.assertEqual(form.is_valid(), True)
      self.assertEqual(form.fields['recordToDevice'].initial, None)
      self.assertEqual(form.fields['filePath'].initial, None)
      self.assertEqual(form.fields['maxSpace'].initial, None)
      self.assertEqual(form.fields['timeToLive'].initial, None)
      self.assertEqual(form.fields['lengthOfRecordings'].initial, None)

