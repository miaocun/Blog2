from django import forms
from .models import Post, Category

from markdownx.widgets import MarkdownxWidget


class CategoryChoiceField(forms.ChoiceField):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.choices = lambda: [(category.name, category.name) for category in Category.objects.all()]

class PostForm(forms.ModelForm):
        def __init__(self,*args,**kwd):
                super(PostForm, self).__init__(*args,**kwd)
                self.fields["created"].required = False

        class Meta:
            model = Post
            fields = ('category','title','content','created')

            category = CategoryChoiceField(label="カテゴリー", widget=forms.Select)

            widget = {
                    'content': MarkdownxWidget(),
                    }

"""
class PostForm(forms.Form):
        title = forms.CharField(label='title', max_length=30)
        content = forms.CharField(label='content', widget=forms.Textarea())
"""

