from django.contrib import admin
from django.db import models
from django.forms import CheckboxSelectMultiple


from .models import (Batch, StandartSample,
                     SpecificationStandart,Document,
                     SpecificationParameter, Employee,
                     Method,
                     )

# Register your models here.
@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ['title', 'volume', 'best_before_date']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}, }


@admin.register(StandartSample)
class StandartSampleAdmin(admin.ModelAdmin):
    list_display = ['title', 'reg_number']


@admin.register(SpecificationStandart)
class SpecificationStandartAdmin(admin.ModelAdmin):
    list_display = [ 'title']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(SpecificationParameter)
class SpecificationParameterAdmin(admin.ModelAdmin):
    list_display = ['title', 'butch_series']

    def butch_series(self, obj):
        return obj.butch_series.title
    butch_series.short_description = 'Номер серии'
    butch_series.admin_order_field = 'butch_series__title'


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    list_display = ['title']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple}, }
