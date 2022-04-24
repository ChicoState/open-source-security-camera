from django import forms

# form to handle file (Video/ Video Poster) upload
class UploadFileForm(forms.Form):
    file = forms.FileField()