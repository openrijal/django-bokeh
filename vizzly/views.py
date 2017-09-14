# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import components


@login_required(login_url='/login/')
def index(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username}
    return render(request, 'index.html', context)


@login_required(login_url='/login/')
def single(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    # some data here
    x = [1, 3, 5, 7, 9, 11, 13]
    y = [1, 2, 3, 4, 5, 6, 7]
    title = 'y = f(x)'

    # plot params
    plot = figure(title=title,
                  x_axis_label='X-Axis',
                  y_axis_label='Y-Axis',
                  plot_width=400,
                  plot_height=400)

    # some plot function
    plot.line(x, y, legend='f(x)', line_width=2)

    # plot = figure()
    # plot.circle([1, 2], [3, 4])

    script, div = components(plot, CDN)

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'script': script, 'div': div}
    return render(request, 'single.html', context)


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
