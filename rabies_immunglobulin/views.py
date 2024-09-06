from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required

import numpy as np

from plotly.offline import plot
import plotly.graph_objs as go

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
        if protocol.standart_samples:
            standart_sample = protocol.standart_samples.title
        else: standart_sample = None
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
            'standart_sample': standart_sample,
            'pk': reference.methods.pk,
                               }
        serialized_protocols.append(serialized_protocol)
    
    return render(
        request,
        "quality_protocol.html",
        context={'protocols': serialized_protocols,
                 'batch': batch,
                 }
        )


def get_batch_docs(request, title):
    docs = Document.objects.filter(series__title=title)
    print(docs)
    if docs:
        return render(
            request, "batch_docs.html",
            context={'status': True,
                     'title': title,
                     'docs': docs}
                      )
    else:
        return render(
        request,"batch_docs.html",
        context={'status': False,
                 'title': title,}
                      )


def get_standart_sample(request, title, date):
    samples = StandartSample.objects.filter(
        indicator__title=title,
        best_before_date__gte = date,
        issue_date__lte = date)
    if samples:
        return render(
            request, "standart_sample.html",
            context={'status': True,
                     'title': title,
                     'date': date,
                     'samples': samples}
                      )
    else:
        return render(
            request,"standart_sample.html",
            context={'status': False,
                     'title': title,
                     'date': date,})
 

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


def f(x_data, b):
    x = np.arange(x_data[0], (x_data[-1] + 1))
    y = 0*x + b
    return y


def get_shuechart_data(specification_title):
    batches = Batch.objects.all().order_by('title')

    sp_standart = SpecificationStandart.objects.get(title=specification_title)
    y_data = []
    x_data = []
    parameters = [batch.batch_parameters.filter(
            title__title__contains=specification_title).values() for batch in batches]
    print(parameters)
    for parameter in parameters:
        if parameter:
            y_data.append(parameter[0]['value'])
            x_data.append(parameter[0]['butch_series_id'])

    r_list = [np.abs(y_data[index] - y_data[index+1]) for index,_ in enumerate(y_data[:-1])]
    x_r = x_data[1:]
    mean_y = float(np.mean(y_data))
    mean_r = float(np.mean(r_list))
    ucl = mean_y + 2.66*mean_r
    lcl = mean_y - 2.66*mean_r
    reference_value = sp_standart.reference_value
    sigma = mean_r/1.128
    c_up = mean_y + sigma
    c_l = mean_y - sigma
    b_up = mean_y + 2*sigma
    b_l = mean_y - 2*sigma
    a_up = mean_y + 3*sigma
    a_l = mean_y - 3*sigma
    r_up = 3.267*mean_r

    return {'y_data': y_data,
            'x_data': x_data,
            'x_data_r': x_r,
            'r_list': r_list,
            'mean_y': mean_y,
            'mean_r': mean_r,
            'ucl': ucl,
            'lcl': lcl,
            'c_up': c_up,
            'b_up': b_up,
            'a_up': a_up,
            'c_l': c_l,
            'b_l': b_l,
            'a_l': a_l,
            'r_up': r_up,
            'reference_value': reference_value,
            }
    

def plot_x_shuechart(shuechart_data, specification_title):
           
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=shuechart_data['y_data'],
        mode='lines+markers', name='Динамика',
        opacity=0.8, marker_color='green',))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['mean_y']),
        name='Среднее значение'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['ucl']),
        name='Верхняя граница'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['lcl']),
        name='Нижняя граница'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['reference_value']),
        name='Среднее нормативное значение'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['c_up']),
        name='c_up'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['c_l']),
        name='c_l'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['b_up']),
        name='b_up'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['b_l']),
        name='b_l'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['a_up']),
        name='a_up'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['a_l']),
        name='a_l'))

    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  title=f"Карта Шухарта X {specification_title}",
                  xaxis_title="Производственные серии",
                  yaxis_title="Значения показателя",
                  xaxis = dict(tickmode = 'linear', dtick = 1),
                  margin=dict(l=0, r=0, t=30, b=0))

    return plot(fig, output_type='div')

def plot_r_shuechart(shuechart_data, specification_title):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data_r'],
        y=shuechart_data['r_list'],
        mode='lines+markers', name='Динамика размаха',
        opacity=0.8, marker_color='green',))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data_r'],
        y=f(shuechart_data['x_data_r'], shuechart_data['mean_r']),
        name='Среднее значение размаха'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data_r'],
        y=f(shuechart_data['x_data_r'], shuechart_data['r_up']),
        name='Верхняя контрольная граница размаха'))

    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  title=f"Карта Шухарта Rm {specification_title}",
                  xaxis_title="Производственные серии",
                  yaxis_title="Значения размаха",
                  xaxis = dict(tickmode = 'linear', dtick = 1),
                  margin=dict(l=0, r=0, t=30, b=0))

    return plot(fig, output_type='div')



def get_graphs(request):

    specifications = SpecificationStandart.objects.all()
    specification_titles = []
    for i in specifications:
        specification_titles.append(i.title)
    specification_title = request.POST.get('specification_obj')
    print(specification_title)
    if specification_title:
        shuechart_data = get_shuechart_data(specification_title)
        print(shuechart_data)
        plot_x = plot_x_shuechart(shuechart_data, specification_title)
        plot_r = plot_r_shuechart(shuechart_data, specification_title)
        context = {
        'specifications': specification_titles,
        'specification_title': specification_title,
        'plot_x' : plot_x,
        'plot_r' : plot_r,
        }
    else:
        context = {
        'specifications': specification_titles,
        'specification_title': [],
        'plot_x' : [],
        'plot_r' : [],
        }    
    return render(request, 'graphs.html', context)
