# Generated by Django 4.2.13 on 2024-09-04 10:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0019_alter_standartsample_indicator_2'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='standartsample',
            name='indicator',
        ),
    ]
