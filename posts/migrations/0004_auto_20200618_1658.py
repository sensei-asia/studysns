# Generated by Django 2.2.13 on 2020-06-18 07:58

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='picture',
            field=imagekit.models.fields.ProcessedImageField(upload_to='image/posts'),
        ),
    ]
