from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

from .models import (Batch, StandartSample,
                     SpecificationStandart,Document,
                     SpecificationParameter, Employee,
                     Method,                     
                     ) 

# Create your views here.
@login_required
def index(request):
    return render(
        request,
        "index.html",
        context={"title": 'БАЗА ДАННЫХ'}
                  )


def get_batches(request):
    batches = Batch.objects.all()
    return render(
        request,
        "batches.html",
        context={'batches': batches}
        )


def get_batch_protocol(request, title):
    batch = Batch.objects.get(title=title)
    serialized_protocols = []
    protocols = batch.batch_parameters.order_by('title')
    for protocol in protocols:
        reference = protocol.title
        serialized_protocol = {
            'title': reference,
            'value': protocol.value,
            'measure': protocol.get_measure_display(),
            'description': protocol.description,
            'controler': protocol.controler,
            'control_date': protocol.control_date,
            'reference_value': reference.reference_value,
            'deviation': reference.deviation,
            'reference_description': reference.reference_description,
            'method': reference.methods.title,
            'media': protocol.media
                               }
        serialized_protocols.append(serialized_protocol)
    
    return render(
        request,
        "quality_protocol.html",
        context={'protocols': serialized_protocols,
                 'batch': batch,
                 }
        )





##def get_batch_protocol(request, title):
##    batch = Batch.objects.get(title=title)
##    protocols = [i for i  in batch.batch_parameters.order_by('title')]
##
##    
##    print(protocols[0].title.upper_limit)
##    
##    return render(
##        request,
##        "quality_protocol.html",
##        context={'protocols': protocols,
##                 }
##        )
