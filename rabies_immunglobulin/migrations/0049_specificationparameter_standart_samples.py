# Generated by Django 4.2.13 on 2025-03-25 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0048_remove_specificationparameter_standart_samples_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specificationparameter',
            name='standart_samples',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='control_appl', to='rabies_immunglobulin.standartsample', verbose_name='Стандартный образец'),
        ),
    ]
