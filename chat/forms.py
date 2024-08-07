from django import forms
from .models import Room, Message
from django.contrib.auth.models import User

class RoomForm(forms.ModelForm):
    is_private = forms.BooleanField(required=False, label="Private Room")
    allowed_users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Allowed Users"
    )

    class Meta:
        model = Room
        fields = ['name', 'is_private', 'allowed_users']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Room.objects.filter(name=name).exists():
            raise forms.ValidationError("A room with this name already exists.")
        return name

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type your message here...', 'rows': 1, 'style': 'resize: none;'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        image = cleaned_data.get('image')

        if not content and not image:
            raise forms.ValidationError("Either content or image must be provided.")
        return cleaned_data

