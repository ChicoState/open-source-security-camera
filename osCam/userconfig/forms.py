from .models import Network, RaspberryPi, Camera, Storage, CameraView
from user.models import CustomUser
from django import forms
from django.forms import ModelForm

# Class for Network Settings
class NetworkEntryForm( ModelForm ):
    homeIpAddress = forms.CharField(label='home ip address', required=False,
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    cameraIpAddress = forms.CharField(label='camera ip address', required=False,
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    homeNetmask = forms.CharField(label='home netmask', required=False,)

    class Meta:
        model = Network
        fields = ('homeIpAddress', 'cameraIpAddress', 'homeNetmask',)

# Class for Camera Settings
class CameraEntryForm( ModelForm ):
    deviceName = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Backyard Cam',
            'class':"form-control"}
        )
    )
    ipAddress = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': '10.0.0.94',
            'class':"form-control"}
        )
    )
    port = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '80',
            'class':"form-control"}
        )
    )
    modelNum = forms.IntegerField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '4',
            'class':"form-control"}
        )
    )
    modelName = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Raspberry Pi',
            'class':"form-control"}
        )
    )
    cameraIndex = forms.IntegerField(
        disabled=True,
        widget=forms.TextInput(attrs={
            'placeholder': '0',
            'class':"form-control"}
        )
    )
    class Meta:
        model = Camera
        fields = (
            'deviceName',
            'ipAddress',
            'port',
            'modelNum',
            'modelName',
        )
    # labels
    def __init__(self, *args, **kwargs):
        super(CameraEntryForm, self).__init__(*args, **kwargs)
        self.fields['deviceName'].label = "Device Name"
        self.fields['ipAddress'].label = "IP Address"
        self.fields['port'].label = "Port"
        self.fields['modelNum'].label = "Model Number"
        self.fields['modelName'].label = "Model Name"
        self.fields['cameraIndex'].label = "Camera Index"

# Class for view settings
# this affects how the 'feed' from the camera is 'viewed'
class CameraViewForm( ModelForm ):
    showMotionBoxes = forms.BooleanField(required=False)
    showContours = forms.BooleanField(required=False)
    showText = forms.BooleanField(required=False)
    text = forms.CharField(max_length=255, required=False)
    contrast = forms.IntegerField(required=False)
    brightness = forms.IntegerField(required=False)

    recording = forms.BooleanField(
        label='enable recording',
        widget=forms.CheckboxInput(),
        required=False)
    fps = forms.ChoiceField(
        choices=((15, '15'), (30, '30'), (60, '60')),)
    invert = forms.BooleanField(
        required=False,
        label='invert image',
        widget=forms.CheckboxInput())
    mirror = forms.BooleanField(
        required=False,
        label='mirror image',
        widget=forms.CheckboxInput())
    codec = forms.ChoiceField(
        choices=(('h264', 'h264'), ('mjpeg', 'mjpeg'), ('avi', 'avi')),)

    class Meta:
        model = CameraView
        fields = (
            'showMotionBoxes',
            'showContours',
            'showText',
            'text',
            'contrast',
            'brightness',
            'recording',
            'fps',
            'invert',
            'mirror',
            'codec',)
    # labels
    def __init__(self, *args, **kwargs):
        super(CameraViewForm, self).__init__(*args, **kwargs)
        self.fields['showMotionBoxes'].label = "Show Motion Boxes"
        self.fields['showContours'].label = "Show Contours"
        self.fields['showText'].label = "Show Text"
        self.fields['text'].label = "Text"
        self.fields['contrast'].label = "Contrast"
        self.fields['brightness'].label = "Brightness"
        self.fields['recording'].label = "Enable Recording"
        self.fields['fps'].label = "FPS"
        self.fields['invert'].label = "Invert Image"
        self.fields['mirror'].label = "Mirror Image"
        self.fields['codec'].label = "Codec"

# class for Storage settings
class StorageForm( ModelForm ):
    recordToDevice = forms.BooleanField(required=False, label='record to device',)
    recordToCloud = forms.BooleanField(required=False, label='record to cloud',)
    filePath = forms.CharField(max_length=255, required=False, label='file path',)
    maxSpace = forms.IntegerField(required=False, label='max space', )
    timeToLive = forms.IntegerField(required=False, label='time to live',)
    archive = forms.BooleanField(required=False, label='archive',)
    lengthOfRecordings = forms.IntegerField(required=False, label='length of record',)
    codec = forms.ChoiceField(
        choices=(('h264', 'h264'), ('mjpeg', 'mjpeg'), ('avi', 'avi')),)

    class Meta:
        model = Storage
        fields = (
            'recordToDevice',
            'recordToCloud',
            'filePath',
            'maxSpace',
            'timeToLive',
            'archive',
            'lengthOfRecordings',
            'codec',)
    # labels
    def __init__(self, *args, **kwargs):
        super(StorageForm, self).__init__(*args, **kwargs)
        self.fields['recordToDevice'].label = "Record to Device"
        self.fields['recordToCloud'].label = "Record to Cloud"
        self.fields['filePath'].label = "File Path"
        self.fields['maxSpace'].label = "Max Space"
        self.fields['timeToLive'].label = "Time to Live"
        self.fields['archive'].label = "Archive"
        self.fields['lengthOfRecordings'].label = "Length of Recordings"
        self.fields['codec'].label = "Codec"

class EmailEntryForm( ModelForm ):
    email = forms.CharField(label='email address', required=False,
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )
    emailKey = forms.CharField(label='email authentication key', required=False,
        widget=forms.TextInput(attrs={'size':'80', 'class':"form-control"})
        )

    class Meta:
        model = CustomUser
        fields = ('email', 'emailKey',)

    # labels
    def __init__(self, *args, **kwargs):
        super(EmailEntryForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['emailKey'].label = "Email Authenticaion Key"
