# Generated by Django 4.2.13 on 2024-12-03 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0040_remove_standartsample_indicator_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='specificationparameter',
            name='standart_samples',
        ),
    ]
