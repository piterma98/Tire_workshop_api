"""Workshop forms."""
# Django
from django import forms
from django.core.exceptions import ValidationError

# Local
from .utils import encode_image_to_base64


class BusinessHourAdminForm(forms.ModelForm):
    """Business hour admin form."""

    def clean(self):  # noqa: D102
        if self.cleaned_data['from_hour'] > self.cleaned_data['to_hour']:
            raise ValidationError('The opening hour must be before closing hour!')
        super(BusinessHourAdminForm, self).clean()


class WorkshopAdminForm(forms.ModelForm):
    """Workshop admin form."""

    image_upload = forms.ImageField(required=False)

    def save(self, commit=True):  # noqa: D102
        instance = super(WorkshopAdminForm, self).save(commit=commit)
        image = self.cleaned_data.get('image_upload', None)
        if image:
            image_upload_base64 = encode_image_to_base64(image.read())
            instance.image = image_upload_base64
        if commit:
            instance.save()
        return instance
