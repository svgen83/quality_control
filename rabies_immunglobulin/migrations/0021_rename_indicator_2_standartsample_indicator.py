# Generated by Django 4.2.13 on 2024-09-04 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0020_remove_standartsample_indicator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='standartsample',
            old_name='indicator_2',
            new_name='indicator',
        ),
    ]
