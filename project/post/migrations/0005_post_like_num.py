# Generated by Django 5.0.7 on 2024-07-16 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_alter_comment_writer'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_num',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
