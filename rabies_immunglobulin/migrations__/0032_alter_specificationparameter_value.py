# Generated by Django 4.2.13 on 2024-09-16 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0031_specificationparameter_begin_control_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specificationparameter',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, verbose_name='Количественное значение'),
        ),
    ]
