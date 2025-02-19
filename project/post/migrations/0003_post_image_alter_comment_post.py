# Generated by Django 5.0.7 on 2024-07-16 11:27

import django.db.models.deletion
import post.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=post.models.image_upload_path),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='post.post'),
        ),
    ]
