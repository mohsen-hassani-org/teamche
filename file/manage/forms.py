from django import forms
from file.models import File

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('file', )