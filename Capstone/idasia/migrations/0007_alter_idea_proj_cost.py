# Generated by Django 4.1.5 on 2023-01-16 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('idasia', '0006_alter_idea_proj_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='proj_cost',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]