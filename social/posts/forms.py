from django import forms
from .models import Post


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'message', 'image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].label = 'Upload image'
        self.fields['message'].widget.attrs.update({'rows': 6})

