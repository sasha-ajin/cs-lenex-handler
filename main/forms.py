from django.forms import Form, FileField
from django.core.validators import FileExtensionValidator


class UploadFileForm(Form):
    file = FileField(validators=[FileExtensionValidator(['xml'])])

    # def clean(self):
    #     file = self.cleaned_data['file']
    #     parser = (et.parse(file)).getroot()
    #     valid = False
    #     for child in parser:
    #         if child.tag == 'MEETS':
    #             valid = True
    #     if not valid:
    #         raise ValidationError('Error')
