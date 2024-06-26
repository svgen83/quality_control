# Generated by Django 4.2.13 on 2024-05-24 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.PositiveSmallIntegerField(verbose_name='Номер серии')),
                ('volume', models.DecimalField(blank='True', decimal_places=3, max_digits=10, verbose_name='Объем серии')),
                ('ampoules_quantity', models.PositiveSmallIntegerField(verbose_name='Количество ампул')),
                ('issue_date', models.DateField(verbose_name='дата выпуска')),
                ('best_before_date', models.DateField(verbose_name='срок годности')),
            ],
            options={
                'verbose_name': 'Производственная серия',
                'verbose_name_plural': 'Производственные серии',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название документации')),
                ('reg_number', models.PositiveIntegerField(verbose_name='Регистрационный номер')),
                ('approval_date', models.DateField(verbose_name='дата утверждения')),
                ('validity', models.DateField(verbose_name='срок действия')),
                ('approving_authority', models.CharField(max_length=200, verbose_name='Кем утверждено')),
                ('doc_type', models.CharField(blank='True', choices=[('Primary', 'Первичная'), ('Secondary', 'Вторичная')], db_index=True, default='Primary', max_length=200, verbose_name='Тип документа')),
            ],
            options={
                'verbose_name': 'Документация',
                'verbose_name_plural': 'Документация',
                'ordering': ['doc_type', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Фамилия, имя, отчество')),
                ('image', models.ImageField(blank=True, null=True, upload_to='media', verbose_name='изображение')),
                ('laboratory', models.CharField(max_length=200, verbose_name='Структурное подразделение')),
                ('job_title', models.TextField(blank=True, verbose_name='Должноcть')),
                ('duties', models.TextField(blank=True, verbose_name='Должноcтные обязанности')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Method',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank='True', max_length=200, verbose_name='Название метода')),
                ('description', models.TextField(blank='True', verbose_name='Описание метода')),
                ('docs', models.ManyToManyField(blank=True, related_name='methods', to='rabies_immunglobulin.document')),
            ],
            options={
                'verbose_name': 'Метод контроля',
                'verbose_name_plural': 'Методы контроля',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='StandartSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название стандартного образца')),
                ('reg_number', models.PositiveIntegerField(verbose_name='Регистрационный номер')),
                ('value', models.DecimalField(blank='True', decimal_places=3, max_digits=10, verbose_name='Значение определяемой характеристики')),
                ('indicator', models.CharField(max_length=200, verbose_name='Определяемая характеристика')),
                ('sample_type', models.CharField(blank='True', choices=[('PH', 'Фармакопейный'), ('RF', 'Государственный'), ('OSO', 'Отраслевой'), ('WHO', 'Стандарт ВОЗ'), ('IN_HOUSE', 'Стандарт предприятия')], db_index=True, default='IN_HOUSE', max_length=200, verbose_name='Вид стандартного образца')),
                ('issue_date', models.DateField(verbose_name='дата выпуска')),
                ('best_before_date', models.DateField(verbose_name='срок годности')),
                ('documents', models.ForeignKey(blank='True', null='True', on_delete=django.db.models.deletion.DO_NOTHING, related_name='sample', to='rabies_immunglobulin.document', verbose_name='документация')),
            ],
            options={
                'verbose_name': 'Стандартный образец',
                'verbose_name_plural': 'Стандартные образцы',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SpecificationStandart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='название спецификационной характеристики')),
                ('measure', models.CharField(max_length=5, verbose_name='единица измерения')),
                ('description', models.CharField(blank='True', max_length=200, verbose_name='Описание характеристики')),
                ('upper_limit', models.DecimalField(blank='True', decimal_places=2, max_digits=10, verbose_name='Максимальное значение')),
                ('lower_limit', models.DecimalField(blank='True', decimal_places=2, max_digits=10, verbose_name='Минимальное значение')),
                ('methods', models.ForeignKey(blank='True', default='Нет метода', on_delete=django.db.models.deletion.DO_NOTHING, related_name='reference_value', to='rabies_immunglobulin.method', verbose_name='Метод определения')),
            ],
            options={
                'verbose_name': 'Референсное значение показателя качества',
                'verbose_name_plural': 'Референсные значения показателей качества',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SpecificationParameter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(blank=True, max_length=200, verbose_name='Количественное значение')),
                ('measure', models.CharField(blank='True', choices=[('No measure', 'Нет размерности'), ('UI', 'Международные единицы'), ('percents', '%'), ('OI', 'Единица оптической плотности'), ('temperature', 'градус Цельсия')], db_index=True, default='No measure', max_length=200, verbose_name='Единица измерения')),
                ('description', models.CharField(blank='True', max_length=200, verbose_name='Описание значения')),
                ('control_date', models.DateField(verbose_name='дата проведения контроля')),
                ('method_doc', models.CharField(blank=True, max_length=200, null=True, verbose_name='Документация с описанием метода контроля')),
                ('butch_series', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='batch_parameters', to='rabies_immunglobulin.batch', verbose_name='Номер серии')),
                ('controler', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='control_carry', to='rabies_immunglobulin.employee', verbose_name='Контролер')),
                ('standart_parameters', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='rabies_immunglobulin.specificationstandart', verbose_name='Нормативные значения')),
                ('standart_samples', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='control_appl', to='rabies_immunglobulin.standartsample', verbose_name='Стандартный образец')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='batch_parameter', to='rabies_immunglobulin.specificationstandart', verbose_name='Определяемая характеристика')),
            ],
            options={
                'verbose_name': 'Значение показателя качества',
                'verbose_name_plural': 'Значения показателей качества',
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='batch',
            name='docs',
            field=models.ManyToManyField(blank=True, related_name='series', to='rabies_immunglobulin.employee'),
        ),
    ]
