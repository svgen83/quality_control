# Generated by Django 4.2.13 on 2024-12-13 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0044_remove_specificationstandart_if_sample'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificationstandart',
            name='if_sample',
            field=models.BooleanField(blank=True, db_index=True, default=False, null=True, verbose_name='Предусмотрен ли стандартный образец'),
        ),
    ]
