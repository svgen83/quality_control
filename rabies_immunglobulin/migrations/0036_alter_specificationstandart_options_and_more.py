# Generated by Django 4.2.13 on 2024-11-28 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rabies_immunglobulin', '0035_alter_standartsample_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='specificationstandart',
            options={'ordering': ['title'], 'verbose_name': 'Нормативное значение показателя качества', 'verbose_name_plural': 'Нормативные значения показателей качества'},
        ),
        migrations.AlterModelOptions(
            name='standartsample',
            options={'ordering': ['title', 'reg_number'], 'verbose_name': 'Стандартный образец', 'verbose_name_plural': 'Стандартные образцы'},
        ),
    ]