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

    plot = figure()
    plot.circle([1, 2], [3, 4])

    script, div = components(plot, CDN)

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'script': script, 'div': div}
    return render(request, 'single.html', context)
