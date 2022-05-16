from .models import Camera, Storage, CameraView, CustomUser
from django import forms
from django.forms import ModelForm


# Class for Camera Settings
class CameraEntryForm(ModelForm):
    deviceName = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Backyard Cam',
                'class': "form-control"
            }
        )
    )

    class Meta:
        model = Camera
        fields = (
            'deviceName',
        )

    # Labels
    def __init__(self, *args, **kwargs):
        super(CameraEntryForm, self).__init__(*args, **kwargs)
        self.fields['deviceName'].label = "Device Name"


# Class for view settings
# This affects how the 'feed' from the camera is 'viewed'
class CameraViewForm(ModelForm):
    showMotionBoxes = forms.BooleanField(required=False)
    showText = forms.BooleanField(required=False)
    text = forms.CharField(max_length=255, required=False)
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
    scale = forms.ChoiceField(
        choices=(
            (1.00, '1.00'),
            (0.75, '0.75'),
            (0.50, '0.50'),
            (0.25, '0.25')
        ),
    )

    class Meta:
        model = CameraView
        fields = (
            'showMotionBoxes',
            'showText',
            'text',
            'fps',
            'invert',
            'mirror',
            'scale',
        )

    # Labels
    def __init__(self, *args, **kwargs):
        super(CameraViewForm, self).__init__(*args, **kwargs)
        self.fields['showMotionBoxes'].label = "Show Motion Boxes"
        self.fields['showText'].label = "Show Text"
        self.fields['text'].label = "Text"
        self.fields['fps'].label = "FPS"
        self.fields['invert'].label = "Invert Image"
        self.fields['mirror'].label = "Mirror Image"
        self.fields['scale'].label = "Scale"


# Class for Storage settings
class StorageForm(ModelForm):
    recordToDevice = forms.BooleanField(
        required=False,
        label='record to device',
    )
    filePath = forms.CharField(
        max_length=255,
        required=False,
        label='file path',
    )
    maxSpace = forms.IntegerField(
        required=False,
        label='max space',
    )
    timeToLive = forms.IntegerField(
        required=False,
        label='time to live',
    )
    lengthOfRecordings = forms.IntegerField(
        required=False,
        label='length of record',
    )

    class Meta:
        model = Storage
        fields = (
            'recordToDevice',
            'filePath',
            'maxSpace',
            'timeToLive',
            'lengthOfRecordings',
        )

    # Labels
    def __init__(self, *args, **kwargs):
        super(StorageForm, self).__init__(*args, **kwargs)
        self.fields['recordToDevice'].label = "Record to Device"
        self.fields['filePath'].label = "File Path"
        self.fields['maxSpace'].label = "Max Space"
        self.fields['timeToLive'].label = "Time to Live"
        self.fields['lengthOfRecordings'].label = "Length of Recordings"


class EmailEntryForm(ModelForm):
    email = forms.CharField(label='email address', required=False,
        widget=forms.TextInput(attrs={'size': '80', 'class': "form-control"}))
    emailKey = forms.CharField(label='email authentication key', required=False,
        widget=forms.TextInput(attrs={'size': '80', 'class': "form-control"}))

    class Meta:
        model = CustomUser
        fields = ('email', 'emailKey',)

    # Labels
    def __init__(self, *args, **kwargs):
        super(EmailEntryForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Email Address"
        self.fields['emailKey'].label = "Email Authenticaion Key"
