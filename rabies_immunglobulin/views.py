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
    protocols = batch.batch_parameters.order_by('title__index_number')
    for protocol in protocols:
        reference = protocol.title
        if reference.reference_sample.all():
            ifsample = True
        else: ifsample = None
        
        control_date = protocol.end_control_date

        serialized_protocol = {
            'title': reference.title,
            'value': protocol.value,
            'measure': protocol.get_measure_display(),
            'description': protocol.description,
            'controler': protocol.controler,
            'control_date': control_date,
            'up_value': reference.upper_limit,
            'low_value': reference.lower_limit,
            'reference_description': reference.reference_description,
            'method': reference.methods.title,
            'media': protocol.media,
            'if_sample': ifsample,
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
        best_before_date__gte=date,
        issue_date__lte=date)

    if samples:
        return render(
            request, "standart_sample.html",
            context={
                'status': True,
                'title': title,
                'date': date,
                'samples': samples})
    else:
        return render(
        request,"standart_sample.html",
        context={'status': False,
                 'title': title,
                 'date': date
                 }
        )


def get_method(request, pk):
    method = Method.objects.get(pk=pk)
    docs = Document.objects.filter(methods=method)
    docs_serialized = [doc for doc in docs]

    return render(
        request,
        "method.html",
        context={'title': method.title,
                 'description': method.description,
                 'docs_serialized': docs_serialized,}
        )


def f(x_data, b):
    x = np.array(x_data)
    y = 0*x + b
    return y


def get_shuechart_data(specification_title):
    batches = Batch.objects.all().order_by('title')

    sp_standart = SpecificationStandart.objects.get(title=specification_title)
    y_data = []
    x_data = []

    parameters = [batch.batch_parameters.filter(
            title__title__contains=specification_title) for batch in batches]

    for parameter in parameters:
        if parameter:
            y_data.append(float(parameter[0].value))
            x_data.append(parameter[0].butch_series.title)

    r_list = [np.abs(y_data[index] - y_data[index+1]) for index,_ in enumerate(y_data[:-1])]
    x_r = x_data[1:]
    mean_y = np.mean(y_data)
    mean_r = np.mean(r_list)
    ucl = mean_y + 2.66*mean_r
    lcl = mean_y - 2.66*mean_r
    up_value = sp_standart.upper_limit
    low_value = sp_standart.lower_limit
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
            'up_value': up_value,
            'low_value': low_value,
            }

def trend_data(y):
    a = np.array([i+1 for i in range(len(y))])
    trend = np.polyfit(a, y, 1)
    equation = np.poly1d(trend)
    return equation(a)

def plot_x_shuechart(shuechart_data, specification_title):
    ticks_x_list = list(map(str, shuechart_data['x_data']))

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=shuechart_data['y_data'],
        mode='lines+markers', name='Паспортные данные',
        opacity=0.8, marker_color='green',))

    fig.add_trace(go.Scatter(x=shuechart_data['x_data'],
        y=trend_data(shuechart_data['y_data']),
        opacity=1, name='Линия тренда', marker_color='black'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['mean_y']),
        name='Центральная линия', marker_color='orange'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['ucl']),
        name='Верхняя контрольная граница',
        marker_color='red'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['lcl']),
        name='Нижняя контрольная граница',
        marker_color='red'))

    if shuechart_data['up_value']:
        fig.add_trace(go.Scatter(
            x=shuechart_data['x_data'],
            y=f(shuechart_data['x_data'], shuechart_data['up_value']),
            name='Максимальное нормативное значение',
            marker_color='blue'))

    if shuechart_data['low_value']:
        fig.add_trace(go.Scatter(
            x=shuechart_data['x_data'],
            y=f(shuechart_data['x_data'], shuechart_data['low_value']),
            name='Минимальное нормативное значение',
            marker_color='blue'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['c_up']),
        name='Верхняя граница зоны С', opacity=0.2, marker_color='grey'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['c_l']),
        name='Нижняя граница зоны С', opacity=0.2, marker_color='grey'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['b_up']),
        name='Верхняя граница зоны В', opacity=0.2, marker_color='grey'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['b_l']),
        name='Нижняя граница зоны В', opacity=0.2, marker_color='grey'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['a_up']),
        name='Верхняя граница зоны А', opacity=0.2, marker_color='grey'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data'],
        y=f(shuechart_data['x_data'], shuechart_data['a_l']),
        name='Нижняя граница зоны А', opacity=0.2, marker_color='grey'))

    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  title=f"Карта Шухарта X - {specification_title}",
                  xaxis_title="Производственные серии",
                  yaxis_title="Значения показателя",
                  xaxis = dict(
                      type='category',
                      tickvals = ticks_x_list),
                  margin=dict(l=0, r=0, t=30, b=0))

    return plot(fig, output_type='div')

def plot_r_shuechart(shuechart_data, specification_title):
    ticks_x_list = list(map(str, shuechart_data['x_data']))

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data_r'],
        y=shuechart_data['r_list'],
        mode='lines+markers', name='Динамика размаха',
        opacity=0.8, marker_color='green',))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data_r'],
        y=f(shuechart_data['x_data_r'], shuechart_data['mean_r']),
        name='Центральная линия размаха', marker_color='orange'))

    fig.add_trace(go.Scatter(
        x=shuechart_data['x_data_r'],
        y=f(shuechart_data['x_data_r'], shuechart_data['r_up']),
        name='Верхняя контрольная граница размаха', marker_color='red'))

    fig.update_layout(legend_orientation="h",
                  legend=dict(x=.5, xanchor="center"),
                  title=f"Карта Шухарта Rm - {specification_title}",
                  xaxis_title="Производственные серии",
                  yaxis_title="Значения размаха",
                  xaxis = dict(
                      type='category',
                      tickvals = ticks_x_list),
                  margin=dict(l=0, r=0, t=30, b=0))

    return plot(fig, output_type='div')



def get_graphs(request):

    specifications = SpecificationStandart.objects.all()
    specification_titles = []
    for i in specifications:
        if i.upper_limit or i.lower_limit:
            specification_titles.append(i.title)
    specification_title = request.POST.get('specification_obj')
    if specification_title:
        shuechart_data = get_shuechart_data(specification_title)
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
