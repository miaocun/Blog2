# Generated by Django 2.2.23 on 2021-05-23 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210523_0233'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('研究', 'research'), ('教育', 'education'), ('その他', 'others')], default='研究', max_length=50),
        ),
    ]
