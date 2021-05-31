from django.db import models
from django.conf import settings
from django.utils import timezone

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
import re

# Create your models here.

class Category(models.Model):
    name = models.CharField("カテゴリー", max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):

    title = models.CharField("タイトル",max_length=200)
    category = models.ForeignKey(Category, verbose_name="カテゴリー",on_delete=models.PROTECT)
    content = MarkdownxField("本文",max_length=500)
    created = models.DateTimeField("作成日",default=timezone.now)

    class Meta:
        ordering = ['-created']


    def convert_markdown_to_html(self):
        return markdownify(self.content)

    def __str__(self):
        return self.title

    def convert_markdown_to_html_shorter(self):
        shorter = re.sub('!\[\]\(.*\)','', self.content) 
        shorter = re.sub('<img .*>', '', shorter)
        return markdownify(shorter[:30]) 
