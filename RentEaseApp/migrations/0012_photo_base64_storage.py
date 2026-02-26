from django.db import migrations, models


def migrate_files_to_base64(apps, schema_editor):
    """Convert existing file-based photos to base64. Skips if file no longer exists."""
    import base64
    from django.conf import settings
    import os

    Photo = apps.get_model('RentEaseApp', 'Photo')
    for photo in Photo.objects.all():
        try:
            old_field = photo.photo
            path = getattr(old_field, 'name', None) if old_field else None
            if not path and isinstance(old_field, str):
                path = old_field
            if path:
                filepath = os.path.join(settings.MEDIA_ROOT, path)
                if os.path.isfile(filepath):
                    with open(filepath, 'rb') as f:
                        photo.photo_data = base64.b64encode(f.read()).decode('utf-8')
                    ext = os.path.splitext(path)[1].lower()
                    content_types = {
                        '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                        '.png': 'image/png', '.gif': 'image/gif',
                        '.webp': 'image/webp',
                    }
                    photo.content_type = content_types.get(ext, 'image/jpeg')
                    photo.save()
        except Exception:
            photo.photo_data = ''
            photo.content_type = 'image/jpeg'
            photo.save()


def reverse_migrate(apps, schema_editor):
    """Cannot reverse base64 to files - no-op."""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('RentEaseApp', '0011_contracttemplate_template_structure'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='content_type',
            field=models.CharField(
                default='image/jpeg',
                help_text='MIME type (e.g. image/jpeg, image/png)',
                max_length=50
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='photo',
            name='photo_data',
            field=models.TextField(
                default='',
                help_text='Base64-encoded image data'
            ),
            preserve_default=False,
        ),
        migrations.RunPython(migrate_files_to_base64, reverse_migrate),
        migrations.RemoveField(
            model_name='photo',
            name='photo',
        ),
    ]
