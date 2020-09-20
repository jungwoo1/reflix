from django import forms
from .models import Review,Detgle
from ckeditor_uploader.widgets import CKEditorUploadingWidget
SPO_CHOICES = [
    ('포함', '포함'),
    ('미포함', '미포함')
]
class CreateReview(forms.ModelForm):
    class Meta:
        model = Review

        fields = ['title','movie_title','genre','spo','content',]

        widgets = {
            'title' : forms.TextInput(
                attrs = {'class': 'form-control', 'style' :'width:100%','placeholder':'리뷰 제목을 입력하세요.'}
            ),
            'movie_title': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width:100%', 'placeholder': '영화 제목을 입력하세요.'}
            ),
            'genre': forms.TextInput(
                attrs={'class': 'form-control', 'style': 'width:100%', 'placeholder': '영화 장르을 입력하세요.'}
            ),
            'spo': forms.Select(
                attrs={'class': 'form-control', 'style': 'width:10%'},
                choices=SPO_CHOICES,
            ),
            'content' : forms.CharField(widget=CKEditorUploadingWidget()),

        }
# class EditReview(forms.ModelForm):
#     class Meta:
#         model = Review
#
#         fields = ['title','movie_title','genre','spo','content']
#
#         widgets = {
#             'title' : forms.TextInput(
#                 attrs = {'class': 'form-control', 'style' :'width:100%','placeholder': model.title}
#             ),
#             'movie_title': forms.TextInput(
#                 attrs={'class': 'form-control', 'style': 'width:100%', 'placeholder': model.movie_title}
#             ),
#             'genre': forms.TextInput(
#                 attrs={'class': 'form-control', 'style': 'width:100%', 'placeholder': model.genre}
#             ),
#             'spo': forms.TextInput(
#                 attrs={'class': 'form-control', 'style': 'width:100%', 'placeholder': model.spo}
#             ),
#             'content' : forms.CharField(widget=CKEditorUploadingWidget())
#         }


class DetgleForm(forms.ModelForm):
    class Meta:
        model = Detgle
        # comment만 입력받기
        fields = ['content']

