from django.db import models
from datetime import date
# Create your models here.
from ckeditor.fields import RichTextField


class Document(models.Model):
    TYPE_CHOICE = (
        ('Primary', 'Первичная'),
        ('Secondary', 'Вторичная'),
    )
    title = models.CharField(max_length=200,
                             verbose_name='название документации')
    reg_number = models.PositiveIntegerField(
        verbose_name='Регистрационный номер')
    approval_date = models.DateField(
        verbose_name='дата утверждения')
    validity = models.DateField(
        verbose_name='срок действия')
    approving_authority = models.CharField(
        max_length=200,
        verbose_name='Кем утверждено')
    doc_type = models.CharField(
        max_length=200,
        verbose_name='Тип документа',
        choices=TYPE_CHOICE,
        default='Primary',
        db_index=True,
        blank=True)
    doc_media = models.FileField(upload_to='media', null=True, blank=True)

    class Meta:
        verbose_name = 'Документация'
        verbose_name_plural = 'Документация'
        ordering = ['doc_type', 'title']

    def __str__(self):
        return self.title


class Method(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название метода', blank=True)
    description = RichTextField(
        verbose_name='Описание метода', blank=True)
    docs = models.ManyToManyField(
        Document,
        related_name='methods',
        verbose_name='Документация с описанием метода',
        blank=True)

    class Meta:
        verbose_name = 'Метод контроля'
        verbose_name_plural = 'Методы контроля'
        ordering = ['title']

    def __str__(self):
        return self.title


class SpecificationStandart(models.Model):
    MEASURE_CHOICE = (
        ('No measure', 'Нет размерности'),
        ('UI', 'Международные единицы в 1 мл'),
        ('percents', '%'),
        ('OI', 'Единица оптической плотности'),
        ('temperature', 'градус Цельсия'),
        ('ml', 'мл'),
        ('pH', 'единица рН'))
    title = models.CharField(
        max_length=200,
        verbose_name='название спецификационной характеристики')
    index_number = models.PositiveIntegerField(
        verbose_name='номер в соответствии с протоколом исследования',
        default=0       
        )
    measure = models.CharField(
        max_length=50,
        verbose_name='единица измерения',
        choices=MEASURE_CHOICE,
        default='No measure',
        db_index=True,
        blank=True)
    reference_description = models.CharField(
        max_length=1000,
        verbose_name='Описание характеристики',
        blank = True, null = True)
    upper_limit = models.DecimalField(
        max_digits = 10,
        decimal_places = 3,
        verbose_name='Максимальное значение',
        blank=True, null = True)
    lower_limit = models.DecimalField(
        max_digits = 10,
        decimal_places = 3,
        verbose_name='Минимальное значение',
        blank=True, null=True)
    methods = models.ForeignKey(Method,
        verbose_name='Метод определения', blank=True,
        on_delete=models.DO_NOTHING,
        related_name='reference_value')

    class Meta:
        verbose_name = 'Нормативное значение показателя качества'
        verbose_name_plural = 'Нормативные значения показателей качества'
        ordering = ['title']

    def __str__(self):
        return self.title


class StandartSample(models.Model):
    TYPE_CHOICE = (
        ('PH', 'Фармакопейный'),
        ('RF', 'Государственный'),
        ('OSO', 'Отраслевой'),
        ('WHO', 'Стандарт ВОЗ'),
        ('IN_HOUSE', 'Стандарт предприятия'),
        ('ST_C', 'Образец сравнения'),
    )
    title = models.CharField(max_length=200,
                             verbose_name='название стандартного образца')
    reg_number = models.PositiveIntegerField(
        verbose_name='Регистрационный номер')
    value = models.DecimalField(
        decimal_places=3,
        max_digits=10,
        verbose_name='Значение определяемой характеристики',
        blank=True)
    description = models.CharField(
        max_length=1000,
        verbose_name='Дополнительные сведения',
        blank = True, null = True)
    sample_type = models.CharField(
        max_length=200,
        verbose_name='Вид стандартного образца',
        choices=TYPE_CHOICE,
        default='IN_HOUSE',
        db_index=True,
        blank=True)
    issue_date = models.DateField(
        verbose_name='дата выпуска')
    best_before_date = models.DateField(
        verbose_name='срок годности')
    documents = models.ForeignKey(Document,
        verbose_name='документация', blank =True,
        on_delete=models.DO_NOTHING, null = True,
        related_name='sample')
    indicator = models.ManyToManyField(
        SpecificationStandart,
        verbose_name='Определяемая характеристика',
        related_name = 'reference_sample')

    class Meta:
        verbose_name = 'Стандартный образец'
        verbose_name_plural = 'Стандартные образцы'
        ordering = ['title','reg_number']

    def __str__(self):
        return self.title


class Employee(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name='Фамилия, имя, отчество')
    image = models.ImageField(verbose_name='изображение',
                              upload_to='media',
                              blank=True, null=True
                              )
    laboratory = models.CharField('Структурное подразделение', max_length=200)
    job_title = models.TextField('Должноcть', blank=True)
    duties = models.TextField('Должноcтные обязанности', blank=True)

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['title']

    def __str__(self):
        return self.title


class Batch(models.Model):
    title = models.PositiveSmallIntegerField(
        verbose_name='Номер серии', unique=True)
    volume = models.DecimalField(
        decimal_places=3,
        max_digits=10,
        verbose_name='Объем серии',
        blank=True)
    ampoules_quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество ампул', blank=True)
    packs_quantity = models.PositiveSmallIntegerField(
        verbose_name='Количество упаковок', blank=True)
    issue_date = models.DateField(
        verbose_name='дата выпуска')
    best_before_date = models.DateField(
        verbose_name='срок годности')
    docs = models.ManyToManyField(
        Document,
        related_name='series',
        blank=True, verbose_name='документация')

    class Meta:
        verbose_name = 'Производственная серия'
        verbose_name_plural = 'Производственные серии'
        ordering = ['title']

    def __str__(self):
        return str(self.title)


class SpecificationParameter(models.Model):
    MEASURE_CHOICE = (
        ('No measure', 'Нет размерности'),
        ('UI', 'Международные единицы в 1 мл'),
        ('percents', '%'),
        ('pH', 'единица рН'),
        ('OI', 'Единица оптической плотности'),
        ('temperature', 'градус Цельсия'))# дублируется

    title = models.ForeignKey(
        SpecificationStandart, on_delete=models.DO_NOTHING,
        verbose_name='Определяемая характеристика',
        related_name='batch_parameter')
    value = models.DecimalField(
        decimal_places=3,
        max_digits=10,
        blank=True,
        verbose_name='Количественное значение')
    measure = models.CharField(
        max_length=50,
        verbose_name='Единица измерения',
        choices=MEASURE_CHOICE,
        default='No measure',
        db_index=True,
        blank=True)
    description = models.TextField(
        verbose_name='Описание значения',
        blank = 'True')
    controler =  models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING,
        related_name='control_carry',
        blank=True,
        verbose_name='Контролер')
    begin_control_date = models.DateField(
        verbose_name='дата начала контроля', default=date.today)
    end_control_date = models.DateField(
        verbose_name='дата проведения контроля',
        default=date.today)
    butch_series = models.ForeignKey(
        Batch, on_delete=models.DO_NOTHING,
        related_name='batch_parameters',
        blank=True, null=True,
        verbose_name='Номер серии')
    media = models.FileField(upload_to='media', null=True, blank=True)

    class Meta:
        verbose_name = 'Значение показателя качества производственной серии'
        verbose_name_plural = 'Значения показателей качества производственных серий'
        ordering = ['title']
        unique_together = ('title', 'butch_series')

    def __str__(self):
        return str(self.title)
