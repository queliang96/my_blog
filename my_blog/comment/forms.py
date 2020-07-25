from django import forms
from .models import Comment
#forms.ModelForm,它适用于需要直接与数据库交互的功能，比如新建、更新数据库的字段等
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']