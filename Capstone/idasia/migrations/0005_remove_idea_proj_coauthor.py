# Generated by Django 4.1.5 on 2023-01-15 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('idasia', '0004_alter_proj_files_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='idea',
            name='proj_coAuthor',
        ),
    ]
