# Generated by Django 4.2.13 on 2024-09-09 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0023_document_doc_media'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='specificationparameter',
            unique_together={('title', 'butch_series')},
        ),
    ]
