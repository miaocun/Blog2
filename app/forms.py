from django import forms
from .models import Post, Category

from markdownx.widgets import MarkdownxWidget

category_data = Category.objects.all()
category_choice = {}
for category in category_data:
        category_choice[category] = category

class PostForm(forms.ModelForm):
        def __init__(self,*args,**kwd):
                super(PostForm, self).__init__(*args,**kwd)
                self.fields["created"].required = False


        class Meta:
            model = Post
            fields = ('category','title','content','created')

            category = forms.ChoiceField(label="カテゴリー", widget=forms.Select, choices = list(category_choice.items()))

            widget = {
                    'content': MarkdownxWidget(),
                    }


"""
class PostForm(forms.Form):
        title = forms.CharField(label='title', max_length=30)
        content = forms.CharField(label='content', widget=forms.Textarea())
"""

