# Generated by Django 4.2.13 on 2024-05-31 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0012_alter_specificationstandart_deviation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificationparameter',
            name='media',
            field=models.FileField(blank=True, null=True, upload_to='media'),
        ),
    ]
