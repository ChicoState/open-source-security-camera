from django import forms

# form to handle file upload
class UploadFileForm(forms.Form):
    file = forms.FileField()