# Generated by Django 5.2.1 on 2025-06-16 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0002_medicamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicamento',
            name='imagen_url',
            field=models.URLField(default='http://example.com'),
            preserve_default=False,
        ),
    ]
