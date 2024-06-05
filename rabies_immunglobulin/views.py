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
            'media': protocol.media,
            'standart_samples': protocol.standart_samples,
            'pk': reference.methods.pk
                               }
        serialized_protocols.append(serialized_protocol)
    
    return render(
        request,
        "quality_protocol.html",
        context={'protocols': serialized_protocols,
                 'batch': batch,
                 }
        )



def get_method(request, pk):
    method = Method.objects.get(pk=pk)
    docs = Document.objects.filter(methods=method)
    docs_serialized = [doc.title for doc in docs]
    print(docs_serialized)

    return render(
        request,
        "method.html",
        context={'title': method.title,
                 'description': method.description,
                 'docs_serialized': docs_serialized}
        )
