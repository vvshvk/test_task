from django import forms
from .models import Picture


class ImageForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'load-image'})
