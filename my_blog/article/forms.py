#引入表单类
from django import forms
#引入文章模型
from .models import ArticlePost
'''class ArticlePostForm(forms.Form):
    title = forms.CharField(label='文章标题',widget=forms.TextInput(attrs={'class':'form-control'}))
    column = forms.CharField(label="栏目",widget=forms.TextInput(attrs={'class':'form-control'}))
    body = forms.CharField(label='文章正文',widget=forms.Textarea(attrs={'class':'form-control','rows':'12'}))'''

#forms.ModelForm,它适用于需要直接与数据库交互的功能，比如新建、更新数据库的字段等
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #指明数据来源
        model = ArticlePost
        #定义表单包含的字段
        fields = ('title','tags','body','avatar')