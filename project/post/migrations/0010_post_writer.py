import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

def set_default_writer(apps, schema_editor):
    User = apps.get_model(settings.AUTH_USER_MODEL)
    Post = apps.get_model('post', 'Post')
    default_user = User.objects.first()
    for post in Post.objects.all():
        if not post.writer_id:
            post.writer = default_user
            post.save()

class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_remove_post_like'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='writer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.RunPython(set_default_writer),
    ]
