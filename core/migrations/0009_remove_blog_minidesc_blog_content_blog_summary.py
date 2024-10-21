# Generated by Django 4.2.11 on 2024-05-03 23:24

import ckeditor.fields
import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0008_alter_blog_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="blog",
            name="minidesc",
        ),
        migrations.AddField(
            model_name="blog",
            name="content",
            field=ckeditor_uploader.fields.RichTextUploadingField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="blog",
            name="summary",
            field=ckeditor.fields.RichTextField(default=1),
            preserve_default=False,
        ),
    ]
