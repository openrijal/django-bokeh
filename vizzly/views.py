# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components

import load_data


@login_required(login_url='/login/')
def index(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username}
    return render(request, 'index.html', context)


# @login_required(login_url='/login/')
# def single(request):
#     is_loggedin = True if request.user.is_authenticated else False
#     is_admin = True if request.user.is_superuser else False
#     username = request.user.username
#     plot_available = False

#     # some data here
#     x = [1, 3, 5, 7, 9, 11, 13]
#     y = [1, 2, 3, 4, 5, 6, 7]
#     title = 'y = f(x)'

#     # plot params
#     plot = figure(title=title,
#                   x_axis_label='X-Axis',
#                   y_axis_label='Y-Axis',
#                   plot_width=400,
#                   plot_height=400)

#     # some plot function
#     plot.line(x, y, legend='f(x)', line_width=2)

#     # plot = figure()
#     # plot.circle([1, 2], [3, 4])

#     script, div = components(plot, CDN)
#     if div:
#         plot_available = True

#     context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available':plot_available, 'script': script, 'div': div}
#     return render(request, 'single.html', context)


@login_required(login_url='/login/')
def single(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username
    plot_available = False
    script = vin = ''

    vin = request.GET.get('vin') if 'vin' in request.GET else None
    if vin:
        data = load_data.load_vin_labeled(vin)

        sqdf_column_dates_type = ["EVENT_OCCURRED"]
        date_format_type = "%Y-%m-%d %H:%M:%S"
        columnsToDate(data, sqdf_column_dates_type, date_format_type)

        print(data)

        # density_time_val = data_sqdf["EVENT_OCCURRED"].dropna().values.astype(np.int64)
        # density_time = gaussian_kde(density_time_val,bw_method='silverman')
        # density_time_interval = np.arange(density_time_val.min(), density_time_val.max(),
        #                             (density_time_val.max() - density_time_val.min()) / 200)
        # density_plot_data = density_time(density_time_interval)
        # density_interval = pd.to_datetime(density_time_interval, format=date_format_type2, errors='coerce')
        # #print(density_interval)

        # plot_dtc_density = figure(plot_width=400, plot_height=400,x_axis_type = "datetime",title="Error codes with respect to time")

        # #############3 Error codes with respect to mileage
        # density_mile_val = data_sqdf["ODO_MILES"].dropna()
        # density_mile = gaussian_kde(density_mile_val,bw_method=0.01)
        # cutoff = 60000
        # density_mile_interval = np.arange(density_mile_val.min(), cutoff,
        #                             (cutoff - density_mile_val.min()) / 200)
        # density_mile_plot_data = density_mile(density_mile_interval)
        # plot_mile_density = figure(plot_width=400, plot_height=400,
        #                         title="Error codes with respect to mileage")



        # # add a line renderer
        # plot_dtc_density.line(density_interval, density_plot_data, color='#ff9900')
        # plot_mile_density.line(density_mile_interval, density_mile_plot_data, color='#ff9900')

        # script, div = components(plot, CDN)
        # if div:
        #     plot_available = True

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available':plot_available, 'script': script, 'div': div}
    return render(request, 'single.html', context)

@login_required(login_url='/login/')
def xglobal(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username
    plot_available = False

    

    script, div = components(plot, CDN)
    if div:
        plot_available = True

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available':plot_available, 'script': script, 'div': div}
    return render(request, 'global.html', context)


@login_required(login_url='/login/')
def sub1(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    plot = figure()
    plot.circle([1, 2], [3, 4])

    script, div = components(plot, CDN)

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'script': script, 'div': div}
    return render(request, 'global.html', context)


@login_required(login_url='/login/')
def sub2(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    # select the tools we want
    TOOLS = "pan,save"

    plot = figure(tools=TOOLS, plot_width=250, plot_height=200)
    plot.circle([1, 7], [5, 9])

    script, div = components(plot, CDN)

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'script': script, 'div': div}
    return render(request, 'global.html', context)
