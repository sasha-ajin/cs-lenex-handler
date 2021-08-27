from django.forms import Form, ModelForm, FileField
from .models import Meet, Club, Athlete
from django.core.exceptions import ValidationError


class UploadFileForm(Form):
    file = FileField()

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file").name.split('.')
        print(file)
        if file[1] != 'xml':
            raise ValidationError('file extension is not xml')

