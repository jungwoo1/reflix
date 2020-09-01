from django import forms
from .models import Review
from ckeditor_uploader.widgets import CKEditorUploadingWidget
class CreateReview(forms.ModelForm):
    class Meta:
        model = Review

        fields = ['title','content']

        widgets = {
            'title' : forms.TextInput(
                attrs = {'class': 'form-control', 'style' : 'width:100%', 'placeholder':'제목을 입력하세요.'}
            ),

            'content' : forms.CharField(widget=CKEditorUploadingWidget()),
        }