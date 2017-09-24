# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from bokeh.resources import CDN
from bokeh.embed import components

import numpy as np
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from scipy.stats import gaussian_kde

from .utils import *

from core.models import SavedPlot


@login_required(login_url='/login/')
@csrf_exempt
def save_session(request):
    user = request.user

    plots = request.POST.get('allPlots')
    name = request.POST.get('canvas_name')
    slug = slugify(name)

    SavedPlot.objects.create(name=name, slug=slug, user=user, plots=plots)

    return HttpResponse("Success", content_type='text/html')


@login_required(login_url='/login/')
def clear_session(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    plot_available = False

    clear_bool = bool(request.GET.get('clear_all')) if 'clear_all' in request.GET else 0

    if clear_bool:
        request.session['session_layouts'] = ''

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plot_available': plot_available,
               'div': '', 'script': ''}
    return render(request, 'global.html', context)


@login_required(login_url='/login/')
def index(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username
    plots = SavedPlot.objects.filter(user=request.user).order_by('-created_on')
    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username, 'plots_count':plots.count()}
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


@login_required(login_url='/login/')
@csrf_exempt
def view_global_ewt(request):
    is_loggedin = True if request.user.is_authenticated else False
    is_admin = True if request.user.is_superuser else False
    username = request.user.username

    context = {'is_loggedin': is_loggedin, 'is_admin': is_admin, 'username': username}
    return render(request, 'global.html', context)


@login_required(login_url='/login/')
@csrf_exempt
def update_plot(request):
    
#   compare_param = request.GET.get('compare_parameter') if 'compare_parameter' in request.GET else ''
#   agg_method = request.GET.get('aggregation_method') if 'aggregation_method' in request.GET else ''
#   agg_param = request.GET.get('aggregation_parameter') if 'aggregation_parameter' in request.GET else ''
    
    plot_type = request.GET.get('plot_type') if 'plot_type' in request.GET else 'pie'
        
    # Common parameters
    x_cat_param = request.GET.get('x_cat_param') if 'x_cat_param' in request.GET else ''
    y_am = request.GET.get('y_am') if 'y_am' in request.GET else ''
    y_ap = request.GET.get('y_ap') if 'y_ap' in request.GET else ''
    x_prim_param = request.GET.get('x_prim_param') if 'x_prim_param' in request.GET else ''
    x_prim_bm = request.GET.get('x_prim_bm') if 'x_prim_bm' in request.GET else ''
    x_prim_bp = request.GET.get('x_prim_bp') if 'x_prim_bp' in request.GET else ''
    
    filter_data = list()
#    pass_freq = 'MONTH'

    layouts_session = list(request.session.get('session_layouts')) if 'session_layouts' in request.session else list()

    binning_param = ''
    eng = tran = miles = ''
    if x_prim_bm == 'date':
        binning_param = "MONTH"
    elif x_prim_bm == 'number':
        binning_param = "1000"
    

    if request.POST:
        eng = request.POST.get('eng') if 'eng' in request.POST else ''
        tran = request.POST.get('tran') if 'tran' in request.POST else ''
        miles = request.POST.get('miles') if 'miles' in request.POST else ''
        x_prim_bp = request.POST.get('x_prim_bp') if 'x_prim_bp' in request.POST else ''
 #       freq = request.POST.get('freq') if 'freq' in request.POST else ''

        if eng:
            filter_data.append({
                "parameter": "ENG",
                "operator": "=",
                "value": eng,
                "type": "string"
            })

        if tran:
            filter_data.append({
                "parameter": "TRAN",
                "operator": "=",
                "value": tran,
                "type": "string"
            })

        if miles:
            filter_data.append({
                "parameter": "MLG",
                "operator": "=",
                "value": miles,
                "type": "string"
            })

        if x_prim_bp:
            binning_param = x_prim_bp
 #       if freq:
 #           pass_freq = freq
            
    json_data = '''
    
      {
	"plot_parameters":{
		"plot_type": "%s",
		"x_axis":{
			"primary" :{
				"parameter": "%s",
				"binning_method": "%s",
				"binning_param" : "%s"
			},
			"categorical":{
				"parameter": "%s"
			}
		},
		"y_axis":{
			"aggregation_method": "%s",
			"aggregation_parameter" : "%s"
		},
		"filters":[
		]
	}
}                         
    ''' % (plot_type, x_prim_param, x_prim_bm, binning_param, x_cat_param, y_am, y_ap)

  #  json_data = '''
  #                  {
  #                      "plot_parameters":{
  #                          "time_scale": "%s",
  #                          "compare_parameter": "%s",
  #                          "aggregation_method": "%s",
  #                          "aggregation_parameter": "%s",
  #                          "filters": []
  #                      }
  #                  }
  #                  ''' % (pass_freq, compare_param, agg_method, agg_param)

    ly = get_layout(json_data, filter_data)

    script, div = components(ly)

    layouts_session.append(div)
    request.session['session_layouts'] = layouts_session

    context = {'script': script, 'div': div,
                'plot_type':plot_type, 'x_prim_param': x_prim_param, 'x_prim_bm': x_prim_bm,
                'x_prim_bp': x_prim_bp, 'x_cat_param': x_cat_param, 'y_am': y_am, 'y_ap': y_ap,
                'eng': eng, 'tran': tran, 'miles':miles}

 #   context = {'script': script, 'div': div, 'cp': compare_param, 'am': agg_method, 'ap': agg_param, 'eng': eng,
 #              'tran': tran, 'miles': miles, 'freq': freq}
    return render(request, 'single.html', context)


@csrf_exempt
def get_iframe(request):
    if request.POST:
        plot_type = request.POST.get('plot_type') if 'plot_type' in request.POST else 'pie'
        
        # Common parameters
        x_cat_param = request.POST.get('x_cat_param') if 'x_cat_param' in request.POST else ''
        y_am = request.POST.get('y_am') if 'y_am' in request.POST else ''
        y_ap = request.POST.get('y_ap') if 'y_ap' in request.POST else ''
        
        querystr = 'plot_type={0}&x_cat_param={1}&y_am={2}&y_ap={3}'.format(plot_type, x_cat_param, y_am, y_ap)
        if plot_type == 'line' or plot_type=='bar':
            x_prim_param = request.POST.get('x_prim_param') if 'x_prim_param' in request.POST else ''
            x_prim_bm = request.POST.get('x_prim_bm') if 'x_prim_bm' in request.POST else ''
            querystr = '{0}&x_prim_param={1}&x_prim_bm={2}'.format(querystr, x_prim_param, x_prim_bm)

        if plot_type == 'bar':
            x_prim_bp = request.POST.get('x_prim_bp') if 'x_prim_bp' in request.POST else ''
            querystr = '{0}&x_prim_bp={1}'.format(querystr, x_prim_bp)


        iframe_html = """
            <iframe width="100%" height="100%" frameborder="0" scrolling="no" onload="resizeIframe(this)"
            src="/update_plot?{0}">
            </iframe><hr />
        """.format(querystr)

        return HttpResponse(iframe_html.strip(), content_type='text/html')

