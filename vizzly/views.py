# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from bokeh.resources import CDN
from bokeh.embed import components
from datetime import datetime

import numpy as np
import pandas
from django.utils.text import slugify
from scipy.stats import gaussian_kde

from .utils import *

from core.models import SavedPlot
        
    
def get_filter_json(filter_obj):
    filter_param= filter_obj.title
    filter_value = filter_obj.value.strip()
    if len(filter_value) <= 0:
        print('Return none for filter')
        return None

    res = '''
        {"parameter":"%s","operator":"=","value":"%s","type":"string"}
        ''' % (filter_param, filter_value)
    print('Returning json for filter: {0}'.format(res))
    return res


def create_figure(time_scale):

    #i_compare_param = compare_param.value
    #i_agg_method = agg_func.labels[agg_func.active]
    #i_time_scale = time_scale.labels[time_scale.active]
    #filters = [eng, trans, vin8]
    i_compare_param = "RPR-DLR"
    i_agg_method = "COUNT"
    i_time_scale = time_scale
    #filters = [eng, trans, vin8]
    i_agg_param = 'AMOUNT(USD)'
    #filter_results = ','.join(list(filter(None.__ne__,[get_filter_json(x) for x in filters])))
    filter_results = ''

    
    json_data = '''
{
"plot_parameters":{
    "time_scale": "%s",
    "compare_parameter": "%s",
    "aggregation_method": "%s",
    "aggregation_parameter": "%s",
    "filters":[%s]
}
}
                        ''' % (i_time_scale, i_compare_param, i_agg_method, i_agg_param, filter_results)
    sql_data = json_to_sql(json_data)
    
    data = get_dataframe(sql_data)
    
    labels = get_plot_labels(json_data)
    columns = data.columns.tolist()
    columns.remove('x')
    x_axis_data = [(x, z) for x in data['x'] for z in columns]
    to_zip = [data[c].tolist() for c in columns]
    y_axis_data = sum(zip(*to_zip), ())
    source = ColumnDataSource(data=dict(x_axis_data=x_axis_data, y_axis_data=y_axis_data))
    
    
    hover = HoverTool(tooltips=[
                        (','.join(labels.x_label.rsplit('-', 1)[::-1]), "@x_axis_data"),
                                        (labels.y_label, "@y_axis_data"),
                                                    ])
    p = figure(x_range=FactorRange(*x_axis_data), plot_width=1200, plot_height=600,title=labels.title, tools=[hover, 'pan', 'box_zoom'])
    #p.x_range = FactorRange(*x_axis_data)
    
    p.vbar(x='x_axis_data', top='y_axis_data', width=1, source=source, line_color="white",
                                fill_color=factor_cmap('x_axis_data', palette=viridis(len(columns)), factors=columns, start=1,
                                                                              end=len(columns)))
    
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = labels.x_label
    p.yaxis.axis_label = labels.y_label
    p.title.align = 'center'
    #source = ColumnDataSource(data=dict(x_axis_data=x_axis_data, y_axis_data=y_axis_data))
    return p



def create_bar_plot(input_json):
    data = get_dataframe(json_to_sql(input_json))
    labels = get_plot_labels(input_json)
    columns = data.columns.tolist()
    columns.remove('x')
    x_axis_data = [(x, z) for x in data['x'] for z in columns]
    to_zip = [data[c].tolist() for c in columns]
    y_axis_data = sum(zip(*to_zip), ())
    source = ColumnDataSource(data=dict(x_axis_data=x_axis_data, y_axis_data=y_axis_data))
    
    
    hover = HoverTool(tooltips=[
                        (','.join(labels.x_label.rsplit('-', 1)[::-1]), "@x_axis_data"),
                                        (labels.y_label, "@y_axis_data"),
                                                    ])
    p = figure(x_range=FactorRange(*x_axis_data), plot_width=1200, plot_height=600,title=labels.title, tools=[hover, 'pan', 'box_zoom'])
    #p.x_range = FactorRange(*x_axis_data)
    
    p.vbar(x='x_axis_data', top='y_axis_data', width=1, source=source, line_color="white",
                                fill_color=factor_cmap('x_axis_data', palette=viridis(len(columns)), factors=columns, start=1,
                                                                              end=len(columns)))
    
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None
    p.xaxis.axis_label = labels.x_label
    p.yaxis.axis_label = labels.y_label
    p.title.align = 'center'
    #source = ColumnDataSource(data=dict(x_axis_data=x_axis_data, y_axis_data=y_axis_data))
    return p


def create_line_plot(input_json):
    request_json = json.loads(input_json)
    data = get_raw_dataframe(json_to_sql(input_json))
    labels = get_plot_labels(input_json)
    print(data.columns)
    #pc = pandas.pivot_table(data, values='y',index='x',columns='z')
    pc = data
    numlines = len(pc.columns)
    mypalette = viridis(numlines)

    col = []
    [col.append(i) for i in pc.columns]

    p = figure( title=labels.title, width = 1200, height = 600)

    if request_json.get('plot_parameters').get('x_axis').get('primary').get('binning_method') == 'date': 
        p = figure( x_axis_type = "datetime", title=labels.title, width = 1200, height = 600)
        if request_json.get('plot_parameters').get('x_axis').get('primary').get('binning_param') == 'DAY':
            fmt_str = '%Y-%m-%d'
        elif request_json.get('plot_parameters').get('x_axis').get('primary').get('binning_param') == 'MONTH':
            fmt_str= '%Y-%m'
    else:
        p = figure( title=labels.title, width = 1200, height = 600)

    p.xaxis.axis_label = labels.x_label
    p.yaxis.axis_label = labels.y_label
    p.title.align = 'center'
    p.y_range.start = 0
    p.x_range.range_padding = 0.1
    p.xaxis.major_label_orientation = 1
    p.xgrid.grid_line_color = None

    for (columnnames, colore) in zip(col, mypalette):
        if request_json.get('plot_parameters').get('x_axis').get('primary').get('binning_method') == 'date': 
            xs = [datetime.strptime(date, fmt_str) for date in pc.index.values.tolist()]
            p.line(xs, pc[columnnames].tolist(),legend = columnnames,  color = colore )
        else:
            p.line(pc.index.values.tolist(), pc[columnnames].tolist(),legend = columnnames,  color = colore )

    
   # hover = HoverTool(tooltips=[
   #                     (','.join(labels.x_label.rsplit('-', 1)[::-1]), "@x_axis_data"),
   #                                     (labels.y_label, "@y_axis_data"),
   #                                                 ])
    
    #source = ColumnDataSource(data=dict(x_axis_data=x_axis_data, y_axis_data=y_axis_data))
    return p



def create_figure_from_json(input_json):

    request_json = json.loads(input_json)

    if request_json.get('plot_parameters').get('plot_type') == "bar":
        return create_bar_plot(input_json)

    if request_json.get('plot_parameters').get('plot_type') == "line":
        return create_line_plot(input_json)



def update_figure(request):
    input_json = request.GET.get('input_json')
    script, div = components(create_figure_from_json(input_json))
    return JsonResponse({"script": script, "div": div})

@login_required(login_url='/login/')
def save_session(request):
    user = request.user
    plots = '<;;>'.join(list(request.session.get('json_in_session')))
    name = request.GET.get('canvas_name')
    slug = slugify(name)

    p = SavedPlot.objects.create(name=name, slug=slug, user=user, plots=plots)

    return render(request, 'view_plot.html', {'plot': p})


@login_required(login_url='/login/')
def clear_session(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    plot_available = False

    clear_bool = bool(request.GET.get('clear_all')) if 'clear_all' in request.GET else 0

    if clear_bool:
        request.session['json_in_session'] = ''

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available,
               'div': '', 'script': ''}
    return render(request, 'global.html', context)


@login_required(login_url='/login/')
def index(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username}
    return render(request, 'index.html', context)


@login_required(login_url='/login/')
def view_single(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username
    plot_available = False
    script = divs = ''

    vin = request.GET.get('vin') if 'vin' in request.GET else None
    if vin:
        data_sqdf = load_vin_labeled(vin)

        sqdf_column_dates_type = ["EVENT_OCCURRED"]
        date_format_type = "%Y-%m-%d %H:%M:%S"
        columnsToDate(data_sqdf, sqdf_column_dates_type, date_format_type)

        print(data_sqdf)

        density_time_val = data_sqdf["EVENT_OCCURRED"].dropna().values.astype(np.int64)
        density_time = gaussian_kde(density_time_val, bw_method='silverman')
        density_time_interval = np.arange(density_time_val.min(), density_time_val.max(),
                                          (density_time_val.max() - density_time_val.min()) / 200)
        density_plot_data = density_time(density_time_interval)
        density_interval = pd.to_datetime(density_time_interval, format=date_format_type, errors='coerce')
        # #print(density_interval)

        plot_dtc_density = figure(plot_width=400, plot_height=400, x_axis_type="datetime",
                                  title="Error codes with respect to time")

        # ############# Error codes with respect to mileage
        density_mile_val = data_sqdf["ODO_MILES"].dropna()
        density_mile = gaussian_kde(density_mile_val, bw_method=0.01)
        cutoff = 60000
        density_mile_interval = np.arange(density_mile_val.min(), cutoff,
                                          (cutoff - density_mile_val.min()) / 200)
        density_mile_plot_data = density_mile(density_mile_interval)
        plot_mile_density = figure(plot_width=400, plot_height=400,
                                   title="Error codes with respect to mileage")

        # # add a line renderer
        plot_dtc_density.line(density_interval, density_plot_data, color='#ff9900')
        plot_mile_density.line(density_mile_interval, density_mile_plot_data, color='#ff9900')

        script, divs = components((plot_dtc_density, plot_mile_density), CDN)
        if divs:
            plot_available = True

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available,
               'script': script, 'divs': divs}
    return render(request, 'single.html', context)


@login_required()
def json_play(request):
    print("DEBUG")
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username
#    print('Data object {0}'.format(request.GET.get('data', None)))
#    if request.GET.get('data', None) == None:
#        plotobj = None
#    else:
#        plotobj = create_figure_from_json(request.GET.get('data').get('input_json'))
#
#
#    script, divs = components(plotobj)

    plot_available = True
    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available}
#               'plot_script': script, 'plot_div': divs}
    return render(request, 'json_play.html', context)




@login_required()
def view_dashboard(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username
    plotobj = create_figure("DAY")

    script, divs = components(plotobj)

    plot_available = True
    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available,
               'plot_script': script, 'plot_div': divs}
    return render(request, 'dashboard.html', context)

@login_required()
def view_global_ewt(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username
    plot_available = False

    plots = list()
    json_array = list(request.session.get('json_in_session')) if 'json_in_session' in request.session else list()

    if request.POST:
        compare_param = request.POST.get('compare_parameter') if 'compare_parameter' in request.POST else ''
        agg_method = request.POST.get('aggregation_method') if 'aggregation_method' in request.POST else ''
        agg_param = request.POST.get('aggregation_parameter') if 'aggregation_parameter' in request.POST else ''

        json_data = '''
            {
                "plot_parameters":{
                    "time_scale": "%s",
                    "compare_parameter": "%s",
                    "aggregation_method": "%s",
                    "aggregation_parameter": "%s",
                    "filters":[]
                }
            }
        ''' % ('MONTH', compare_param, agg_method, agg_param)

        json_array.append(json_data)
        request.session['json_in_session'] = json_array

        for jd in json_array:
            ly = get_layout(jd)
            plots.append(ly)

    script, divs = components(tuple(plots))

    if divs:
        plot_available = True

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available,
               'script': script, 'divs': divs}
    return render(request, 'global.html', context)

# @login_required(login_url='/login/')
# def bar_colormapped(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#
#     plot_available = False
#
#     fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
#     counts = [5, 3, 4, 2, 4, 6]
#
#     source = ColumnDataSource(data=dict(fruits=fruits, counts=counts))
#
#     p = figure(x_range=fruits, plot_height=350, toolbar_location=None, title="Fruit Counts")
#     p.vbar(x='fruits', top='counts', width=0.9, source=source, legend="fruits",
#            line_color='white', fill_color=factor_cmap('fruits', palette=Spectral6, factors=fruits))
#
#     p.xgrid.grid_line_color = None
#     p.y_range.start = 0
#     p.y_range.end = 9
#     p.legend.orientation = "horizontal"
#     p.legend.location = "top_center"
#
#     script, div = components(p)
#
#     if div:
#         plot_available = True
#
#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available,
#                'script': script, 'div': div}
#     return render(request, 'generic_chart.html', context)
#
#
# @login_required(login_url='/login/')
# def bar_nested_colormapped(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#
#     plot_available = False
#
#     colors = ["red", "orange", "yellow", "cyan", "magenta", "#e97cfd", "#c969cc", "#878dcf", "#ec4d70",
#               "#a9d0d3", "#918cbf", "#e85d30"]
#
#     data = plot1_example().pivot_table(values='Claims', index='Month', columns='Dealer').fillna(0).reset_index()
#
#     columns = data.columns.tolist()
#     columns.remove('Month')
#
#     source = ColumnDataSource(data)
#
#     p = figure(x_range=list(source.data['Month']), plot_width=1200, title="something")
#
#     for i in range(-2, len(columns) - 2):
#         p.vbar(x=dodge('Month', i / (len(columns) + 1), range=p.x_range), top=columns[i], width=0.12, source=source,
#                color=colors[i])
#
#     p.y_range.start = 0
#     p.x_range.range_padding = 0.1
#     p.xaxis.major_label_orientation = 1
#     p.xgrid.grid_line_color = None
#
#     script, div = components(p)
#
#     if div:
#         plot_available = True
#
#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available,
#                'script': script, 'div': div}
#     return render(request, 'generic_chart.html', context)
#
#
# @login_required(login_url='/login/')
# def bar_stacked(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#
#     plot_available = False
#
#     fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
#     years = ["2015", "2016", "2017"]
#     colors = ["#c9d9d3", "#718dbf", "#e84d60"]
#
#     data = {'fruits': fruits,
#             '2015': [2, 1, 4, 3, 2, 4],
#             '2016': [5, 3, 4, 2, 4, 6],
#             '2017': [3, 2, 4, 4, 5, 3]}
#
#     source = ColumnDataSource(data=data)
#
#     p = figure(x_range=fruits, plot_height=350, title="Fruit Counts by Year",
#                toolbar_location=None, tools="")
#
#     p.vbar_stack(years, x='fruits', width=0.9, color=colors, source=source,
#                  legend=[value(x) for x in years])
#
#     p.y_range.start = 0
#     p.x_range.range_padding = 0.1
#     p.xgrid.grid_line_color = None
#     p.axis.minor_tick_line_color = None
#     p.outline_line_color = None
#     p.legend.location = "top_left"
#     p.legend.orientation = "horizontal"
#
#     script, div = components(p)
#
#     if div:
#         plot_available = True
#
#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available,
#                'script': script, 'div': div}
#     return render(request, 'generic_chart.html', context)
#
#
# @login_required(login_url='/login/')
# def bar_nested(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#
#     plot_available = False
#
#     fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
#     years = ['2015', '2016', '2017']
#
#     data = {'fruits': fruits,
#             '2015': [2, 1, 4, 3, 2, 4],
#             '2016': [5, 3, 3, 2, 4, 6],
#             '2017': [3, 2, 4, 4, 5, 3]}
#
#     # this creates [ ("Apples", "2015"), ("Apples", "2016"), ("Apples", "2017"), ("Pears", "2015), ... ]
#     x = [(fruit, year) for fruit in fruits for year in years]
#     counts = sum(zip(data['2015'], data['2016'], data['2017']), ())  # like an hstack
#
#     source = ColumnDataSource(data=dict(x=x, counts=counts))
#
#     p = figure(x_range=FactorRange(*x), plot_height=350, title="Fruit Counts by Year",
#                toolbar_location=None, tools="")
#
#     p.vbar(x='x', top='counts', width=0.9, source=source)
#
#     p.y_range.start = 0
#     p.x_range.range_padding = 0.1
#     p.xaxis.major_label_orientation = 1
#     p.xgrid.grid_line_color = None
#
#     script, div = components(p)
#
#     if div:
#         plot_available = True
#
#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username,
#                'plot_available': plot_available,
#                'script': script, 'div': div}
#     return render(request, 'generic_chart.html', context)
#
#
# @login_required(login_url='/login/')
# def bar_mixed(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#
#     plot_available = False
#
#     factors = [
#         ("Q1", "jan"), ("Q1", "feb"), ("Q1", "mar"),
#         ("Q2", "apr"), ("Q2", "may"), ("Q2", "jun"),
#         ("Q3", "jul"), ("Q3", "aug"), ("Q3", "sep"),
#         ("Q4", "oct"), ("Q4", "nov"), ("Q4", "dec"),
#
#     ]
#
#     p = figure(x_range=FactorRange(*factors), plot_height=350,
#                toolbar_location=None, tools="")
#
#     x = [10, 12, 16, 9, 10, 8, 12, 13, 14, 14, 12, 16]
#     p.vbar(x=factors, top=x, width=0.9, alpha=0.5)
#
#     p.line(x=["Q1", "Q2", "Q3", "Q4"], y=[12, 9, 13, 14], color="red", line_width=2)
#
#     p.y_range.start = 0
#     p.x_range.range_padding = 0.1
#     p.xaxis.major_label_orientation = 1
#     p.xgrid.grid_line_color = None
#
#     script, div = components(p)
#
#     if div:
#         plot_available = True
#
#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username,
#                'plot_available': plot_available,
#                'script': script, 'div': div}
#     return render(request, 'generic_chart.html', context)
#
#
# @login_required(login_url='/login/')
# def hide_glyph(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#
#     plot_available = False
#
#     p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
#     p.title.text = 'Click on legend entries to hide the corresponding lines'
#
#     for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
#         df = pd.DataFrame(data)
#         df['date'] = pd.to_datetime(df['date'])
#         p.line(df['date'], df['close'], line_width=2, color=color, alpha=0.8, legend=name)
#
#     p.legend.location = "top_left"
#     p.legend.click_policy = "hide"
#
#     script, div = components(p)
#
#     if div:
#         plot_available = True
#
#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username,
#                'plot_available': plot_available,
#                'script': script, 'div': div}
#     return render(request, 'generic_chart.html', context)
#
#
# @login_required(login_url='/login/')
# def mute_glyph(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#
#     plot_available = False
#
#     p = figure(plot_width=800, plot_height=250, x_axis_type="datetime")
#     p.title.text = 'Click on legend entries to mute the corresponding lines'
#
#     for data, name, color in zip([AAPL, IBM, MSFT, GOOG], ["AAPL", "IBM", "MSFT", "GOOG"], Spectral4):
#         df = pd.DataFrame(data)
#         df['date'] = pd.to_datetime(df['date'])
#         p.line(df['date'], df['close'], line_width=2, color=color, alpha=0.8,
#                muted_color=color, muted_alpha=0.2, legend=name)
#
#     p.legend.location = "top_left"
#     p.legend.click_policy = "mute"
#
#     script, div = components(p)
#
#     if div:
#         plot_available = True
#
#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username,
#                'plot_available': plot_available,
#                'script': script, 'div': div}
#     return render(request, 'generic_chart.html', context)
#
#
# @login_required(login_url='/login/')
# def slider_widget(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#
#     plot_available = False
#
#     x = [x * 0.005 for x in range(0, 200)]
#     y = x
#
#     source = ColumnDataSource(data=dict(x=x, y=y))
#
#     plot = figure(plot_width=400, plot_height=400)
#     plot.line('x', 'y', source=source, line_width=3, line_alpha=0.6)
#
#     callback = CustomJS(args=dict(source=source), code="""
#         var data = source.data;
#         var f = cb_obj.value
#         x = data['x']
#         y = data['y']
#         for (i = 0; i < x.length; i++) {
#             y[i] = Math.pow(x[i], f)
#         }
#         source.change.emit();
#     """)
#
#     slider = Slider(start=0.1, end=4, value=1, step=.1, title="power")
#     slider.js_on_change('value', callback)
#
#     layout = column(slider, plot)
#     script, div = components(layout)
#
#     if div:
#         plot_available = True
#
#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username,
#                'plot_available': plot_available,
#                'script': script, 'div': div}
#     return render(request, 'generic_chart.html', context)
