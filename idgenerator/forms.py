import datetime
from django import forms
from .models import Student

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.images import get_image_dimensions


class StudentForm(forms.ModelForm):
    MAX_LOGO_WIDTH = 4  # cm
    MAX_LOGO_HEIGHT = 4  # cm
    MAX_PHOTO_WIDTH = 3.5  # cm
    MAX_PHOTO_HEIGHT = 4.5  # cm

    class Meta:
        model = Student
        fields = ['first_name', 'middle_name', 'last_name', 'date_of_birth', 'institution', 'logo', 'photo']
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(1900, 2100)),
        }
        help_texts = {
            'first_name': 'Enter your first name',
            'middle_name': 'Enter your middle name (if any)',
            'last_name': 'Enter your last name',
            'date_of_birth': 'Enter your date of birth',
            'institution': 'Enter your institution name',
            'logo': 'Upload your institution logo (maximum size: 4cm x 4cm)',
            'photo': 'Upload your photo (maximum size: 3.5cm x 4.5cm)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'date_of_birth':
                field.widget.attrs.update({'class': 'form-control'})
                field.label = False
            else:
                field.widget = forms.SelectDateWidget(years=range(1900, datetime.date.today().year+1))
                field.widget.attrs.update({'class': 'form-control'})
        self.fields['logo'].widget.attrs.update({'class': 'form-control-file'})
        self.fields['photo'].widget.attrs.update({'class': 'form-control-file'})

    def clean_logo(self):
        logo = self.cleaned_data.get('logo')
        if not logo:
            return logo
        w, h = get_image_dimensions(logo)
        if w > self.MAX_LOGO_WIDTH * 100 or h > self.MAX_LOGO_HEIGHT * 100:
            raise ValidationError(_('Logo image is too large. Maximum size: %(width)scm x %(height)scm'),
                                  params={'width': self.MAX_LOGO_WIDTH, 'height': self.MAX_LOGO_HEIGHT})
        return logo

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            return photo
        w, h = get_image_dimensions(photo)
        if w > self.MAX_PHOTO_WIDTH * 100 or h > self.MAX_PHOTO_HEIGHT * 100:
            raise ValidationError(_('Photo image is too large. Maximum size: %(width)scm x %(height)scm'),
                                  params={'width': self.MAX_PHOTO_WIDTH, 'height': self.MAX_PHOTO_HEIGHT})
        return photo
