# Generated by Django 4.2.13 on 2024-05-24 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0006_alter_specificationparameter_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specificationparameter',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, verbose_name='Количественное значение'),
        ),
    ]
